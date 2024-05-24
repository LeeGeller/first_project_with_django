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
from catalog.models import Product, ContactsData, VersionProduct


class HomeListView(LoginRequiredMixin, ListView):
    model = Product
    fields = (
        "product_name",
        "price",
    )
    template_name = "catalog/home.html"
    login_url = "users:login"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)

        # prefetch_related для оптимизации запросов к базе данных,
        # чтобы получить все связанные объекты VersionProduct для каждого Product
        # При помощи Prefetch (предварительная выборка):
        # versionproduct_set - формсет модели VersionProduct
        # queryset - набор запросов (в данном случае устанавливаем фильтр, чтобы получать
        # только активные версии)

        products_with_versions = Product.objects.prefetch_related(
            Prefetch(
                "versionproduct_set",
                queryset=VersionProduct.objects.filter(is_active_version=True),
            )
        ).all()

        # Добавляем эту отфильтрованную информацию в контекст
        context_data["products_with_versions"] = products_with_versions
        user = self.request.user

        if not user.has_perm("catalog.cancel_product"):
            context_data["products_with_versions"] = context_data["object_list"].filter(
                is_active=True
            )

        return context_data


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
