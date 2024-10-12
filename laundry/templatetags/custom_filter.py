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
    return variable.filter(status_available=True, status_health=True).count()

# Reserve_machine
@register.filter
def reserve_sort_wait_workable(reserve):
    return reserve.filter(status__in=(0,1))

@register.filter
def reserve_sort(reserve):
    return reserve.order_by('-status', 'arrive_at', 'actual_arrive')

@register.filter
def current_reserve_work_til(machine):
    return Reserve_Machine.objects.get(machine=machine, status=2).working_til()

@register.filter
def machine_not_in_state_working(machine):
    return Reserve_Machine.objects.get(machine=machine)

@register.filter
def machine_working(machine):
    return Reserve_Machine.objects.get(machine=machine, status=2).code

@register.filter
def calculate_piece(capacity):
    return (capacity-1)*5