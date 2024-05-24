from django import forms

from catalog.models import Product, VersionProduct

STOP_WORDS = [
    "казино",
    "криптовалюта",
    "крипта",
    "биржа",
    "дешево",
    "бесплатно",
    "обман",
    "полиция",
    "радар",
]


class MixinForms(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"


class ProductForms(MixinForms, forms.ModelForm):
    class Meta:
        model = Product
        fields = (
            "product_name",
            "product_description",
            "image_preview",
            "price",
            "connection_with_category",
        )

    def clean_product_name(self, *args, **kwargs):
        cleaned_data = self.cleaned_data.get("product_name")
        if cleaned_data in STOP_WORDS:
            raise forms.ValidationError("Такой товар не продают на нашей площадке.")
        else:
            return cleaned_data

    def clean_product_description(self, *args, **kwargs):
        cleaned_data = self.cleaned_data.get("product_description")

        if cleaned_data in STOP_WORDS:
            raise forms.ValidationError("Такой товар не продают на нашей площадке.")
        else:
            return cleaned_data


class VersionProductForm(MixinForms, forms.ModelForm):
    class Meta:
        model = VersionProduct
        exclude = ("is_active_version",)


class ProductModeratorForms(MixinForms, forms.ModelForm):
    class Meta:
        model = Product
        fields = ("product_description", "connection_with_category")

    def clean_product_description(self, *args, **kwargs):
        cleaned_data = self.cleaned_data.get("product_description")

        if cleaned_data in STOP_WORDS:
            raise forms.ValidationError("Такой товар не продают на нашей площадке.")
        else:
            return cleaned_data
