# Django
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.http import JsonResponse
from django.db.models import Count

## Exception
from django.core.exceptions import PermissionDenied

## Function Model
from django.db import transaction
from django.db.models import F, IntegerField
from django.db.models.functions import Cast

from django.utils.timezone import now, timedelta, make_aware

# Python
from json import loads
from string import ascii_letters
from datetime import datetime
from random import randint

# Model
from laundry_model.models import *
from laundry.forms import *

# Decorator
from .decorators import access_only

# Authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator

@transaction.atomic
def reserve_check_working():
    for reserve_m in Reserve_Machine.objects.filter(status=2):
        if reserve_m.machine != None:
            reserve_work = reserve_m.working_til()
            machine = Machine.objects.get(pk=reserve_m.machine.id)
            if now() > reserve_work:
                machine.status_available = True
                reserve_m.status = 3
                reserve_m.save()
                machine.save()

def random_string(length=0):
    text = ""
    random_ = ascii_letters+"0123456789"
    for _ in range(length):
        text += random_[randint(0, 62)]
    return text

class Index(View):
    def get(self, request):
        machine_size = Machine_Size.objects.order_by("capacity")
        return render(request, "index.html", {"machine_size": machine_size})

# Customer
@method_decorator(access_only("cus"), name="get")
@method_decorator(access_only("cus"), name="post")
@method_decorator(access_only("cus"), name="put")
class ViewReserve(LoginRequiredMixin, View):
    def get(self, request):
        reserve_check_working()
        review = ReviewReserveForm()
        
        reserve_machine = Reserve_Machine.objects.filter(user=request.user).order_by("status", "-arrive_at", '-work_at')
        return render(request, "customer/view_reserve.html", {
            "reserve_machine": reserve_machine, "sidebar": "sidebar_item/customer.html",
            "form_review": review
        })
    
    def post(self, request):
        review = ReviewReserveForm(request.POST)
        if review.is_valid():
            review.save()
        return redirect("view_reserve")

    # Cancel Reserve
    def put(self, request):
        content = loads(request.body)
        try:
            machine = Reserve_Machine.objects.get(pk=content['machine_id'])
            machine.status = 4
            machine.save()
        except Reserve_Machine.DoesNotExist:
            return JsonResponse({"success": False}, status=500)
        return JsonResponse({"success": True}, status=200)
        
@method_decorator(access_only("cus"), name="get")
@method_decorator(access_only("cus"), name="post")
class ReserveMachineView(LoginRequiredMixin, View):
    def data(self, form = ReserveMachineForm()):
        machine_size = Machine_Size.objects.order_by("capacity")
        machine = []
        for i in machine_size:
            machine.append(i.machine_set.filter(status_available=True))
        time = now() + timedelta(minutes=30)
        return {"form": form, "machine_size": machine_size, "machine":machine, "min_time_reserve": time}
    
    def get(self, request):
        return render(request, "customer/reserve.html", self.data())
    
    def post(self, request):
        form = ReserveMachineForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    cost = 0
                    code = ""
                    arrive_at = form.cleaned_data.get("arrive_at")
                    machine_size = Machine_Size.objects.get(pk=request.POST.get("machine_size"))
                    service = form.cleaned_data.get("service")
                    
                    initial_time = list(map(int, request.POST.get("initial_time").split(" ")))
                    initial_time = make_aware(datetime(*initial_time))
                    
                    if arrive_at < initial_time:
                        raise Exception()
                    
                    cost += machine_size.cost
                    for i in service:
                        cost += i.price
                    
                    code = random_string(6)
                    while Reserve_Machine.objects.filter(status__in=(0, 1), code=code).count():
                        code = random_string(6)
                    
                    reserve_m = Reserve_Machine.objects.create(user=request.user, machine_size=machine_size, 
                                    code=code, cost=cost, arrive_at=arrive_at)
                    reserve_m.service.add(*service)
                    
                    return redirect("view_reserve")
            except Exception:
                raise PermissionDenied()
        return render(request, "customer/reserve.html", self.data(form))

# Staff
@method_decorator(access_only(["stf", "mgr"]), name="get")
@method_decorator(access_only(["stf", "mgr"]), name="put")
class ManageReserve(LoginRequiredMixin, View):
    def get(self, request):
        reserve_check_working()
        getMachines = Machine.objects.annotate(group=F("code")[0]).annotate(number=F("code")[2:]).annotate(number_int=Cast("number", output_field=IntegerField())).order_by("machine_size__capacity", "group", "number_int")

        machine_size = Machine_Size.objects.order_by("capacity")
        reserved = Reserve_Machine.objects.filter(status__range=(0 , 2)).order_by("-status", "actual_arrive" ,"arrive_at")
        
        return render(request, "staff/manage_reserve.html", {"machine_size": machine_size, 'machines': getMachines, "reserved": reserved, 'time_now': now()})
    
    def put(self, request):
        data = loads(request.body)
        # change waiting to workable
        if 'reserve_id' in data:
            reserve_id = data.get('reserve_id')
            change_wating= Reserve_Machine.objects.get(pk=reserve_id)
            change_wating.status = 1
            change_wating.save()
            return JsonResponse({'success': True, 'id': change_wating.id}, status=200)
        
        def changeMachineStatus(machine_code, new_status):
            get_machine = Machine.objects.get(code=machine_code)
            get_machine.status_available = new_status
            get_machine.save()
            return get_machine

        # put workable to machine
        if 'reserve_code_workable' in data:
            reserve_code = data.get('reserve_code_workable')

            if reserve_code in Reserve_Machine.objects.filter(status=1).values_list('code', flat=True):
                
                change_workable = Reserve_Machine.objects.get(code=reserve_code)

                change_workable.work_at = datetime.now()
                change_workable.machine = changeMachineStatus(data.get('machine_code'), 0)
                change_workable.status = 2
                change_workable.save()

                return JsonResponse({'valid': True, 'reserve_code': reserve_code}, status=200)
            return JsonResponse({'valid': False}, status=400)

        # change machine to avalible
        if 'machine_code_avaliable' in data:
            changeMachineStatus(data.get('machine_code_avaliable'), 1)

        # reset machine status
        if 'resetMachine' in data:
            machine_code = data.get('resetMachine')
            change_working= Reserve_Machine.objects.get(machine__code=machine_code, status=2)
            change_working.status = 1
            change_working.save()
            
        return JsonResponse({'valid': True}, status=200)

    def delete(self, request):
        data = loads(request.body)
        reserve_id = data.get('reserve_id')
        reserve = get_object_or_404(Reserve_Machine, id=reserve_id)
        reserve.status = 4
        reserve.save()
        return JsonResponse({'success': True}, status=204)

# Manager
## count all data (use in sidebar)
def count_all_data():
    count_data = {
        "count_staff": Users.objects.exclude(status=0).count(), #Users.objects.filter(role__in = ("stf", "mgr")).exclude(status=0).count()
        "count_machine": Machine.objects.count(),
        "count_size": Machine_Size.objects.count(),
        "count_service": Service.objects.count(),
        "sidebar": "sidebar_item/manager.html"
        }
    return count_data

## Report
class ReportView(View):
    # @method_decorator(login_required)
    def get(self, request):
        return render(request, "manager/report.html")

## Manage User
@method_decorator(access_only("mgr"), name="get")
@method_decorator(access_only("mgr"), name="post")
class AddStaffView(LoginRequiredMixin, View):
    def get(self, request):
        query = request.GET.get('search', '')
        if query:
            getUsers = Users.objects.filter(email__icontains=query).order_by("-role")
        else:
            getUsers = Users.objects.order_by("-status", "-role") #defalut/empty search

        count_data = count_all_data()
        form = AddStaffForm()
        show = {'users': getUsers, 
                'form': form,
                **count_data}
        return render(request, 'manager/add_staff.html', show)
    
    def post(self, request):
        data = loads(request.body)
        user_id = data.get('user_id')
        getUser = Users.objects.get(id=user_id)
        
        # Check for status update
        if 'status' in data:
            new_status = data.get('status')
            print("update_status user_id", user_id, "new_status value", new_status)
            getUser.status = new_status
            # Update user status in the database here
            # Example: User.objects.filter(id=user_id).update(status=status)

        # Check for role update
        if 'role' in data:
            new_role = data.get('role')
            print("update_role user_id", user_id, "new_role value", new_role)
            getUser.role = new_role
            # Update user role in the database here
            # Example: User.objects.filter(id=user_id).update(role=role)
        getUser.save()
        return JsonResponse({'message': 'User updated successfully!'})

## Machine
@method_decorator(access_only("mgr"), name="get")
@method_decorator(access_only("mgr"), name="post")
@method_decorator(access_only("mgr"), name="put")
class AddMachineView(LoginRequiredMixin, View):
    
    def show_data(self, get_getMachine, get_form): ##use this method because when there is an error -> table will disappear
        count_data = count_all_data()
        show = {
            "machines" : get_getMachine,
            "form" : get_form,
            **count_data 
            }
        return show

    def get(self, request):
        getMachines = Machine.objects.annotate(group=F("code")[0]).annotate(number=F("code")[2:]).annotate(number_int=Cast("number", output_field=IntegerField())).order_by("machine_size__capacity", "group", "number_int")
        form = AddMachineForm()
        show = self.show_data(getMachines, form)
        show['machine_size'] = Machine_Size.objects.order_by("capacity")
        return render(request, "manager/add_machine.html", show)
    
    def post(self, request):
        form = AddMachineForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("add_machine")

        getMachines = Machine.objects.annotate(group=F("code")[0]).annotate(number=F("code")[2:]).annotate(number_int=Cast("number", output_field=IntegerField())).order_by("machine_size__capacity", "group", "number_int")
        show = self.show_data(getMachines, form)
        show['machine_size'] = Machine_Size.objects.all()
        return render(request, "manager/add_machine.html", show)
    
    
    def put(self, request):
        content = loads(request.body)
        try:
            with transaction.atomic():
                machine = Machine.objects.get(pk=content['machine_id'])
                if (content['size'] != ""):
                    machine.machine_size = Machine_Size.objects.get(pk=content['size'])
                else:
                    machine.machine_size = None
                machine.status_health = content['status']
                machine.save()
        except Machine.DoesNotExist:
            return JsonResponse({"success": False}, status=500)
        except Machine_Size.DoesNotExist:
            return JsonResponse({"success": False}, status=500)
        except Exception:
            return JsonResponse({"error": True}, status=500)
        return JsonResponse({"success": True}, status=200)
    
    def delete(self, request):
        content = loads(request.body)
        try:
            machine = get_object_or_404(Machine, pk=content['machine_id'])
            machine.delete()
        except KeyError:
            return JsonResponse({"success": False}, status=500)
        return JsonResponse({"success": True}, status=204)

## Size
@method_decorator(access_only("mgr"), name="get")
@method_decorator(access_only("mgr"), name="post")
class AddSizeView(LoginRequiredMixin, View):
    # @method_decorator(login_required)
    def get(self, request):
        # check order (asc, desc) request
        order = request.GET.get('order', 'asc') # first order
        if order == "asc":
            getSizes = Machine_Size.objects.order_by("capacity") # order by asc
        else:
            getSizes = Machine_Size.objects.order_by("-capacity") # order by desc

        count_data = count_all_data()

        show = {"request": request, #request object will be accessible in the temp
                "sizes": getSizes, 
                "form" : AddSizeForm(),
                **count_data
                }
        return render(request, "manager/add_size.html", show)
    
    # @method_decorator(login_required)
    def post(self, request):
        form = AddSizeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add_size') # refresh page for show new inserted data
        print(form.errors)
        return render(request, "manager/add_size.html", {"form": form}) # stay in same page and still fill data
    

    def put(self, request):
        data = loads(request.body)
        cost = data.get('price')
        size_id = data.get('size_id')

        print("cost =", cost, " size_id =", size_id)

        try:
            # Fetch the option and update its price
            option = Machine_Size.objects.get(id=size_id)
            option.cost = cost
            option.save()
            return JsonResponse({'success': True, 'price': option.price}, status=200)
        except Service.DoesNotExist:
            return JsonResponse({'error': 'Option not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    
    def delete(self, request):
        content = loads(request.body)
        try:
            size_machine = get_object_or_404(Machine_Size, pk=content['size_id'])
            size_machine.delete()
        except KeyError:
            return JsonResponse({"success": False}, status=500)
        return JsonResponse({"success": True}, status=204)

## Option
@method_decorator(access_only("mgr"), name="get")
@method_decorator(access_only("mgr"), name="post")
@method_decorator(access_only("mgr"), name="put")
class AddOptionView(LoginRequiredMixin, View):
    # @method_decorator(login_required)
    def show_data(self, get_request, get_getOptions, get_form): ##use this method because when there is an error -> table will disappear
        count_data = count_all_data()
        show = {
            "request": get_request,# request object will be accessible in the template
            "options" : get_getOptions,
            "form" : get_form,
            **count_data 
            }
        return show

    def get(self, request):
        # check order (asc, desc) request
        order = request.GET.get('order', 'asc') # first order
        if order == 'asc':
            getOptions = Service.objects.order_by("price") # order by desc
        else:
            getOptions = Service.objects.order_by("-price") # order by asc

        form = AddOptionForm()
        show = self.show_data(request, getOptions, form) ##content to show

        return render(request, "manager/add_option.html", show)
    
    def post(self, request):
        form = AddOptionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("add_option")
        
        table = Service.objects.order_by("price")
        show = self.show_data(request, table, form)
        return render(request, "manager/add_option.html", show)

    # def put(self, request, option_id, price) update data using with javascript
    def put(self, request):
        data = loads(request.body)
        price = data.get('price')
        option_id = data.get('content_id')

        try:
            # Fetch the option and update its price
            option = Service.objects.get(id=option_id)
            option.price = price
            option.save()
            return JsonResponse({'success': True, 'price': option.price}, status=200)
        except Service.DoesNotExist:
            return JsonResponse({'error': 'Option not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    def delete(self, request):
        content = loads(request.body)
        try:
            option = get_object_or_404(Service, pk=content['option_id'])
            option.delete()
        except KeyError:
            return JsonResponse({"success": False}, status=500)
        return JsonResponse({"success": True}, status=204)