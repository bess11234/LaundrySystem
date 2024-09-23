from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect
from django.views import View
from django.http import JsonResponse

import json
from django.utils.decorators import method_decorator

from laundry_model.models import *
from laundry.forms import *
from .decorators import access_only

class Index(View):
    def get(self, request):
        return render(request, "index.html")
# Customer

# Staff


# Manager

## count all data (use in sidebar)
def count_all_data():
    count_data = {
        "count_staff": Users.objects.filter(role__in = ("stf", "mgr")).exclude(status=0).count(),
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

## Staff
class AddStaffView(View):
    def get(self, request):
        query = request.GET.get('search', '')
        if query:
            getUsers = Users.objects.filter(email__icontains=query).order_by("create_at")
        else:
            getUsers = Users.objects.all().order_by("-status", "create_at") #defalut/empty search

        count_data = count_all_data()
        form = AddStaffForm()
        show = {'users': getUsers, 
                'form': form,
                **count_data}
        return render(request, 'manager/add_staff.html', show)
    
    def post(self, request):
        data = json.loads(request.body)
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
class AddMachineView(View):
    # @method_decorator(login_required)
    def show_data(self, get_getMachine, get_form): ##use this method because when there is an error -> table will disappear
        count_data = count_all_data()
        show = {
            "machines" : get_getMachine,
            "form" : get_form,
            **count_data 
            }
        return show

    @method_decorator(login_required)
    @method_decorator(access_only("mgr"))
    def get(self, request):
        getMachines = Machine.objects.all().order_by("create_at")

        form = AddMachineForm()
        show = self.show_data(getMachines, form)

        return render(request, "manager/add_machine.html", show)
    
    def post(self, request):
        form = AddMachineForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("add_machine")

        show = self.show_data(Machine.objects.all(), form)
        return render(request, "manager/add_machine.html", show)
    
    
    def put(self, request):
        data = json.loads(request.body) ## update machine price
        price = data.get('price')
        machine_id = data.get('machine_id')
        try:
            # Fetch the option and update its price
            machine = Machine.objects.get(id=machine_id)
            machine.cost = price
            machine.save()
            return JsonResponse({'success': True, 'price': machine.cost}, status=200)
        except Service.DoesNotExist:
            return JsonResponse({'error': 'Option not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

class DeleteMachineView(View):
    def get(self, request, machine_id):
        getMachine = Machine.objects.get(id=machine_id)
        getMachine.delete()
        return redirect("add_machine")
        

## Size
class AddSizeView(View):
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

## Delete Size
class DeleteSizeView(View):
    # @method_decorator(login_required)
    def get(self, request, size_id):
        getSize = Machine_Size.objects.get(pk=size_id)
        getSize.delete()
        return redirect("add_size")
    
## Option
class AddOptionView(View):
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
    
    # @method_decorator(login_required)
    def post(self, request):
        form = AddOptionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("add_option")
        
        print(form.errors)
        table = Service.objects.order_by("price")
        show = self.show_data(request, table, form)
        return render(request, "manager/add_option.html", show)

    # def put(self, request, option_id, price) update data using with javascript

    def put(self, request, *args, **kwargs):
        data = json.loads(request.body)
        price = data.get('price')
        option_id = data.get('option_id')

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



class DeleteOptionView(View):
    # @method_decorator(login_required)
    def get(self, request, option_id):
        getOption = Service.objects.get(pk=option_id)
        getOption.delete()
        return redirect("add_option")
