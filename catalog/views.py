from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db.models import Prefetch
from django.forms import inlineformset_factory
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    ListView,
    DetailView,
    UpdateView,
    DeleteView,
)

from catalog.forms import ProductForms, VersionProductForm, ProductModeratorForms
from catalog.models import Product, ContactsData, VersionProduct, Category
from catalog.services import get_category_from_cache


class HomeListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = "catalog/home.html"
    login_url = "users:login"
    context_object_name = 'products_with_versions'

    def get_queryset(self):
        # Получаю id категории из URL
        pk = self.kwargs.get('pk')

        if pk:
            # Фильтрую продукты по категории
            queryset = Product.objects.filter(connection_with_category=pk)
        else:
            # Если категория не указана, показываю все продукты
            queryset = Product.objects.all()

        # Оптимизация запроса
        queryset = queryset.prefetch_related(
            Prefetch(
                "versionproduct_set",
                queryset=VersionProduct.objects.filter(is_active_version=True),
            )
        )

        # Фильтрация по активности продуктов для пользователей без соответствующих прав
        user = self.request.user
        if not user.has_perm("catalog.cancel_product"):
            queryset = queryset.filter(is_active=True)

        return queryset

class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    template_name = "catalog/categories_list.html"
    login_url = "users:login"
    context_object_name = 'categories'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_category'] = self.kwargs.get('pk')
        return get_category_from_cache


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product


class ContactsListView(ListView):
    model = ContactsData


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForms

    success_url = reverse_lazy("catalog:home")

    def form_valid(self, form):
        product = form.save()
        user = self.request.user

        product.owner = user
        product.save()

        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForms

    success_url = reverse_lazy("catalog:home")

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        SubjectFormset = inlineformset_factory(
            Product, VersionProduct, form=VersionProductForm, extra=1
        )
        if self.request.method == "POST":
            context_data["formset"] = SubjectFormset(
                self.request.POST, instance=self.object
            )
        else:
            context_data["formset"] = SubjectFormset(instance=self.object)
        return context_data

    def form_valid(self, form):
        formset = self.get_context_data()["formset"]
        self.object = form.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()
        return super().form_valid(form)

    def get_form_class(self):
        user = self.request.user
        if user == self.object.owner:
            return ProductForms
        if (
                user.has_perm("catalog.change_product_description")
                or user.has_perm("catalog.change_category_product")
                or user.has_perm("catalog.cancel_product")
        ):
            return ProductModeratorForms
        raise PermissionDenied


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product

    success_url = reverse_lazy("catalog:home")
