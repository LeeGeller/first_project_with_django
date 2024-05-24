# Generated by Django 5.0.3 on 2024-04-16 16:08

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="BlogPost",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=150, verbose_name="Заголовок")),
                ("slug", models.CharField(max_length=150, verbose_name="URL")),
                ("text_area", models.TextField()),
                (
                    "image_preview",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="blog/",
                        verbose_name="Изображение",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        default=datetime.datetime.now, verbose_name="Дата создания"
                    ),
                ),
                (
                    "actual_version_indicator",
                    models.BooleanField(default=True, verbose_name="Статус публикации"),
                ),
                ("number_of_views", models.IntegerField(default=0)),
            ],
            options={
                "verbose_name": "Статья",
                "verbose_name_plural": "Статьи",
            },
        ),
    ]
