from django import template

register = template.Library()

@register.filter
def order_toggle(order):
    if order == "desc":
        return 'asc'
    return 'desc'
@register.filter
def machine_is_available_count(variable):
    return variable.filter(status_available=True).count()