from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from config import settings
from servicies import email_verification
from users.apps import UsersConfig
from django.conf.urls.static import static

from users.forms import CustomPasswordResetForm
from users.views import UsersCreateView, PasswordResetView

app_name = UsersConfig.name

urlpatterns = [
    path("login/", LoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", UsersCreateView.as_view(), name="register"),
    path(
        "password-reset/",
        PasswordResetView.as_view(form_class=CustomPasswordResetForm),
        name="password_reset",
    ),
    path(
        "confirm-register/<str:token>/",
        email_verification,
        name="confirm-register",
    ),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
