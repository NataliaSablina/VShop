from django import template

register = template.Library()


@register.filter
def products_number(category_products):
    category_products_2 = category_products[0:8]
    return category_products_2
