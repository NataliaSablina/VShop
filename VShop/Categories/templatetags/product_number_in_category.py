from django import template

register = template.Library()


@register.filter
def products_number_in_category(category_products):
    print(category_products)
    return category_products.count() > 1
