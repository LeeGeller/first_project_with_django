from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from blog.models import BlogPost
from catalog.models import Product, Category
from config import settings
from users.models import Users
from django.apps import apps


@login_required
def toggle_activity(request, model, pk):
    if model == 'Product':
        model_class = Product
        success_url = 'catalog:home'
    elif model == 'BlogPost':
        model_class = BlogPost
        success_url = 'blog:blogpost_list'
    else:
        raise ValueError("Invalid model name provided.")

    obj = get_object_or_404(model_class, pk=pk)

    if hasattr(obj, 'is_active'):
        obj.is_active = not obj.is_active
    elif hasattr(obj, 'actual_version_indicator'):
        obj.actual_version_indicator = not obj.actual_version_indicator

    obj.save()

    return redirect(success_url)


def email_verification(request, token):
    user = get_object_or_404(Users, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse("users:login"))


def get_category_from_cache(request, pk):
    if settings.CACHE_ENABLED:
        key = "categories_with_products"
        cache_data = cache.get(key)
        if cache_data is None:
            category_queryset = Category.objects.prefetch_related('product_set').filter(pk=pk).all()
            cache.set(key, category_queryset)
            return category_queryset
        return cache_data
    else:
        return Category.objects.prefetch_related('product_set').filter(pk=pk).all()
