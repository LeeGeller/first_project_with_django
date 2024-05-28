from django import template

from catalog.models import Category

register = template.Library()


@register.inclusion_tag("catalog/categories_list.html", takes_context=True)
def get_category_items(context):
    categories = Category.objects.all()

    result_list = [{"pk": 0, "category_name": "Все категории"}]

    for category in categories:
        result_list.append({"pk": category.pk, "category_name": category.category_name})

    return {"categories_menu": result_list}
