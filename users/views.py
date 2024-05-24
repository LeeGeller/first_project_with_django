import secrets

from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, FormView

from config.settings import EMAIL_HOST_USER, DEFAULT_FROM_EMAIL
from users.forms import UsersRegisterForm
from users.models import Users


class UsersCreateView(CreateView):
    model = Users
    form_class = UsersRegisterForm
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.token = secrets.token_hex(7)
        user.save()

        host = self.request.get_host()
        url = f"http://{host}/users/confirm-register/{user.token}/"

        send_mail(
            subject="Подтвверди почту",
            message=f"Перейдите по ссылке, чтобы подтвердить вашу электронную почту: {url}",
            from_email=DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
        )
        return super().form_valid(form)


def email_verification(request, token):
    user = get_object_or_404(Users, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse("users:login"))


class PasswordResetView(FormView):
    template_name = "password_reset.html"
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):

        email = form.cleaned_data["email"]

        user = Users.objects.get(email=email)

        new_password = Users.objects.make_random_password()

        user.set_password(new_password)
        user.save()

        send_mail(
            subject="Новый пароль",
            message=f"Вот он: {new_password}",
            from_email=EMAIL_HOST_USER,
            recipient_list=[email],
        )

        return super().form_valid(form)
