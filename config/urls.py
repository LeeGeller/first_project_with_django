from django.conf import settings
from django.conf.urls.static import static
from django.urls import include


from django.contrib import admin
from django.urls import path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("catalog.urls", namespace="catalog")),
    path("blogdata_list/", include("blog.urls", namespace="blog")),
    path("users/", include("users.urls", namespace="users")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
