from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from blog.apps import BlogConfig
from blog.views import (
    BlogListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
)
from sercicies import toggle_activity

app_name = BlogConfig.name

urlpatterns = [
    path("blogpost_list/", BlogListView.as_view(), name="blogpost_list"),
    path("<int:pk>/", PostDetailView.as_view(), name="post"),
    path("create/", PostCreateView.as_view(), name="create_post"),
    path("<int:pk>/update/", PostUpdateView.as_view(), name="update_post"),
    path("<int:pk>/delete/", PostDeleteView.as_view(), name="delete_post"),
    path("activity/<int:pk>/", toggle_activity, name="toggle_activity"),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
