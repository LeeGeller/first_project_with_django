from django import template

from catalog.models import Category

register = template.Library()


@register.inclusion_tag("catalog/category_list.html", takes_context=True)
def get_category_items(context):
    categories_with_products = Category.objects.prefetch_related('product_set').all()

    result_dict = {"Все категории": []}

    for category in categories_with_products:
        product_list = list(category.product_set.all())
        result_dict[category.category_name] = product_list
        result_dict["Все категории"].extend(product_list)

    return {"categories_menu": result_dict}
