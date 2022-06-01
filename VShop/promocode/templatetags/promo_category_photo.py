from django import template

register = template.Library()


@register.filter
def promo_category_photo(category):
    product = category.product_category.first().photo.url
    return product


@register.filter
def promo_category_name(category):
    product = category.product_category.first().promo_code.name
    return product


@register.filter
def get_promo_id_from_category(category):
    promo_code_id = category.product_category.first().promo_code.id
    product_id = category.product_category.first().id
    return promo_code_id


@register.filter
def get_product_id_from_category(category):
    product_id = category.product_category.first().id
    return product_id
