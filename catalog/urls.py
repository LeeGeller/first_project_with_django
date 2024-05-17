from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.views.decorators.cache import cache_page

from catalog.apps import MainappConfig
from catalog.views import (
    ProductDetailView,
    HomeListView,
    ContactsListView,
    ProductCreateView,
    ProductUpdateView,
    ProductDeleteView,
    toggle_activity,
)
from sercicies import toggle_activity

app_name = MainappConfig.name

urlpatterns = [
    path("", cache_page(60)(HomeListView.as_view()), name="home"),
    path("contactsdata_list/", ContactsListView.as_view(), name="contacts"),
    path("<int:pk>/product_detail/", ProductDetailView.as_view(), name="product"),
    path("create_product/", ProductCreateView.as_view(), name="create_product"),
    path(
        "<int:pk>/update_product/", ProductUpdateView.as_view(), name="update_product"
    ),
    path(
        "<int:pk>/delete_product/", ProductDeleteView.as_view(), name="delete_product"
    ),
    path("activity/<int:pk>/", toggle_activity, name="toggle_activity"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
