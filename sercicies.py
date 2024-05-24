from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse

from blog.models import BlogPost
from catalog.models import Product
from users.models import Users


def toggle_activity(request, model, pk):
    obj = get_object_or_404(model, pk=pk)
    if hasattr(obj, 'is_active'):
        obj.is_active = not obj.is_active
    elif hasattr(obj, 'actual_version_indicator'):
        obj.actual_version_indicator = not obj.actual_version_indicator
    obj.save()

    if model == Product:
        return redirect(reverse("catalog:home"))
    elif model == BlogPost:
        return redirect(reverse("blog:blogpost_list"))


def email_verification(request, token):
    user = get_object_or_404(Users, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse("users:login"))
