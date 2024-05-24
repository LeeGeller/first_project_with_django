from django.contrib import admin

from blog.models import BlogPost


@admin.register(BlogPost)
class BlogPostView(admin.ModelAdmin):
    list_display = (
        "title",
        "slug",
        "text_area",
        "image_preview",
        "created_at",
        "actual_version_indicator",
        "number_of_views",
    )
