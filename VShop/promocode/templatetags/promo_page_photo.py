from django import template

register = template.Library()


@register.filter
def promo_photo(promo_code):
    product = promo_code.product_promo.first().photo.url
    return product


@register.filter
def promo_product_id(promo_code):
    product = promo_code.product_promo.first()
    if product:
        return product.id
    return 1


@register.filter
def promo_product_name(promo_code):
    product = promo_code.product_promo.first().name
    return product
