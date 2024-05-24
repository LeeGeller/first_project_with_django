from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Users(AbstractUser):
    username = None
    email = models.EmailField(
        max_length=50, verbose_name="Email", help_text="Введите свой email", unique=True
    )
    avatar = models.ImageField(
        upload_to="users/", verbose_name="Аватар", blank=True, null=True
    )
    phone = PhoneNumberField(
        verbose_name="Телефон",
        help_text="Введите свой номер телефона",
        unique=True,
        blank=True,
        null=True,
    )
    country = models.CharField(
        max_length=150, verbose_name="Страна", help_text="Введите свою страну"
    )
    token = models.CharField(max_length=20, verbose_name="Token", blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def clean(self):
        super().clean()
        if self.country.capitalize() != "Россия":
            raise ValidationError("Страна должна быть: Россия")

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
