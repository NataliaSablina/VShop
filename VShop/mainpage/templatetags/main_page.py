from django import template
from Categories.models import ProductPhoto, Product
register = template.Library()


@register.filter
def product_photos(product):
    product_photos = ProductPhoto.objects.filter(product=product)
    return product_photos