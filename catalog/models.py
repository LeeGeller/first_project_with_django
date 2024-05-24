from django.utils import timezone

from django.db import models

from users.models import Users

NULLABLE = {"blank": True, "null": True}


class NewUser(models.Model):
    first_name = models.CharField(max_length=100, verbose_name="Имя")
    last_name = models.CharField(max_length=50, verbose_name="Фамилия")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"
        ordering = ("last_name",)


class Category(models.Model):
    category_name = models.CharField(max_length=100, verbose_name="Название категории")
    category_description = models.TextField(verbose_name="Описание категории")

    def __str__(self):
        return f"{self.category_name} {self.category_description}"

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "категории"


class Product(models.Model):
    product_name = models.CharField(max_length=100, verbose_name="Название продукта")
    product_description = models.TextField(verbose_name="Описание продукта")
    image_preview = models.ImageField(
        upload_to="catalog/", verbose_name="превью", **NULLABLE
    )
    price = models.DecimalField(
        decimal_places=2, max_digits=10, verbose_name="Цена за покупку"
    )
    created_at = models.DateTimeField(
        default=timezone.now, verbose_name="Дата создания"
    )
    updated_at = models.DateTimeField(
        default=timezone.now, verbose_name="Дата последнего изменения"
    )
    connection_with_category = models.ForeignKey(
        Category, verbose_name="Категория", on_delete=models.SET_NULL, null=True
    )
    slug = models.CharField(max_length=255, verbose_name="URL", **NULLABLE)
    owner = models.ForeignKey(
        Users, on_delete=models.SET_NULL, verbose_name="Владелец", null=True, blank=True
    )
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return (
            f"{self.product_name} {self.product_description} "
            f"{self.image_preview} {self.price} "
            f"{self.created_at} {self.updated_at}"
        )

    class Meta:
        verbose_name = "продукт"
        verbose_name_plural = "продукты"
        permissions = [
            ("cancel_product", "Can cancel product"),
            ("change_product_description", "Can change product description"),
            ("change_category_product", "Can change category product"),
        ]


class ContactsData(models.Model):
    city = models.CharField(max_length=50, verbose_name="Страна")
    identity_nalog_number = models.IntegerField(verbose_name="ИНН")
    addres = models.TextField(verbose_name="Адрес")
    slug = models.CharField(max_length=255, verbose_name="URL", **NULLABLE)

    def __str__(self):
        return f"{self.city} {self.identity_nalog_number} {self.addres}"

    class Meta:
        verbose_name = "Контакт"
        verbose_name_plural = "Контакты"


class VersionProduct(models.Model):
    product = models.ForeignKey(
        Product,
        verbose_name="Продукт",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    number_of_version = models.PositiveIntegerField(
        verbose_name="Номер версии продукта"
    )
    name_of_versions = models.CharField(max_length=150, verbose_name="Название версии")
    is_active_version = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.product}"

    class Meta:
        verbose_name = "Версия"
        verbose_name_plural = "Версии"
