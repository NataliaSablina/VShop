from django import template

from Categories.models import Product
from cart.cart import Cart

register = template.Library()


# @register.filter
# def quantity(product_id):
#     cart = Cart(request)
#     return category_products.count() > 1

@register.simple_tag
def quantity(request, product_id):
    print(product_id.id)
    cart = Cart(request)
    return cart.get(product_id)
