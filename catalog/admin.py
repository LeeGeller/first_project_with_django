from django.contrib import admin

from catalog.models import NewUser, Category, Product, ContactsData, VersionProduct

# Register your models here.
admin.site.register(NewUser)


@admin.register(Category)
class CategoryView(admin.ModelAdmin):
    list_display = (
        "id",
        "category_name",
    )


@admin.register(Product)
class CategoryView(admin.ModelAdmin):
    list_display = (
        "id",
        "product_name",
        "price",
        "connection_with_category",
    )
    list_filter = ("connection_with_category",)
    search_fields = (
        "product_name",
        "product_description",
    )


@admin.register(ContactsData)
class ContactsDataView(admin.ModelAdmin):
    list_display = (
        "city",
        "identity_nalog_number",
        "addres",
    )


@admin.register(VersionProduct)
class VersionProductView(admin.ModelAdmin):
    list_display = (
        "product",
        "number_of_version",
        "name_of_versions",
        "is_active_version",
    )
