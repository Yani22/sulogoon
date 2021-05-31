from django import template

register = template.Library()

@register.simple_tag()
def multiply(qty, unit_price, *args, **kwargs):
    # you would need to do any localization of the result here
    dist = 0
    dist += qty * unit_price

    return dist