from django.contrib.auth.forms import UserCreationForm
from django import forms

from catalog.forms import MixinForms
from users.models import Users


class UsersRegisterForm(MixinForms, UserCreationForm):
    class Meta:
        model = Users
        fields = (
            "email",
            "country",
            "avatar",
            "password1",
            "password2",
        )


class CustomPasswordResetForm(forms.Form):
    email = forms.EmailField(
        label="Email", max_length=254, help_text="Введите email для отправки"
    )
