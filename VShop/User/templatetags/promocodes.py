from django import template

register = template.Library()


@register.filter
def promo_color(sailing_percent, value):
    return sailing_percent <= value
