from django.db import models
from django.utils import timezone


class BlogPost(models.Model):
    title = models.CharField(max_length=150, verbose_name="Заголовок")
    slug = models.CharField(max_length=150, verbose_name="URL", blank=True, null=True)
    text_area = models.TextField(verbose_name="Текст")
    image_preview = models.ImageField(
        upload_to="blog/", verbose_name="Изображение", blank=True, null=True
    )
    created_at = models.DateTimeField(
        default=timezone.now, verbose_name="Дата создания", blank=True, null=True
    )
    actual_version_indicator = models.BooleanField(
        default=True, verbose_name="Статус публикации", blank=True, null=True
    )
    number_of_views = models.IntegerField(default=0, blank=True, null=True)

    def __str__(self):
        return (
            f"{self.title} {self.slug} {self.text_area}"
            f"{self.image_preview} {self.created_at} {self.actual_version_indicator}"
            f"{self.number_of_views}"
        )

    class Meta:
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"
