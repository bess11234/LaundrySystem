from django import template

register = template.Library()

@register.filter
def order_toggle(order):
    if order == "desc":
        return 'asc'
    return 'desc'