from django import template

from laundry_model.models import Reserve_Machine

register = template.Library()

@register.filter
def order_toggle(order):
    if order == "desc":
        return 'asc'
    return 'desc'

@register.filter
def machine_is_available_count(variable):
    return variable.filter(status_available=True).count()

# Reserve_machine
@register.filter
def reserve_sort_wait_workable(reserve):
    return reserve.filter(status__in=(0,1))

@register.filter
def reserve_sort(reserve):
    return reserve.order_by('-status', 'arrive_at', 'actual_arrive')

@register.filter
def current_reserve_work_til(machine):
    return Reserve_Machine.objects.get(machine=machine, status=3).working_til()