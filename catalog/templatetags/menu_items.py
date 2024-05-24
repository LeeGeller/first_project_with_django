from django import template

register = template.Library()


@register.inclusion_tag("catalog/menu_list.html")
def get_menu():
    menu = [
        {"id": 1, "name": "Каталог", "template": "catalog:home"},
        {"id": 2, "name": "Контакты", "template": "catalog:contacts"},
        {"id": 3, "name": "Блог", "template": "blog:blogpost_list"},
    ]
    return {"menu": menu}


@register.inclusion_tag("users/users_list.html", takes_context=True)
def get_users_menu(context):
    request = context.get("request")
    if request.user.is_authenticated:
        users_menu = [
            {"id": 3, "name": "Выйти", "template": "users:logout"},
        ]
    else:
        users_menu = [
            {"id": 1, "name": "Войти", "template": "users:login"},
            {"id": 2, "name": "Регистрация", "template": "users:register"},
        ]
    return {"users_menu": users_menu}
