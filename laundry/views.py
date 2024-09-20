from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect
from django.views import View

from django.utils.decorators import method_decorator

#import model form laundry_model app
from laundry_model.models import *

# import form
from laundry.forms import *

class Index(View):
    def get(self, request):
        return render(request, "index.html")
# Customer

# Staff


# Manager

## count all data (use in sidebar)
def count_all_data():
    count_data = {
        "count_staff": Users.objects.filter(role="staff").count(),
        "count_machine": Machine.objects.count(),
        "count_size": Machine_Size.objects.count(),
        "count_service": Service.objects.count()
        }
    return count_data

## Report
class ReportView(View):
    # @method_decorator(login_required)
    def get(self, request):
        return render(request, "manager/report.html")

## Machine
class AddMachineView(View):
    # @method_decorator(login_required)
    def get(self, request):
        return render(request, "manager/add_machine.html")

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
    def get(self, request):
        # check order (asc, desc) request
        order = request.GET.get('order', 'asc') # first order
        if order == 'asc':
            getOptions = Service.objects.order_by("price") # order by desc
        else:
            getOptions = Service.objects.order_by("-price") # order by asc

        count_data = count_all_data()
        show = {
            "request": request,# request object will be accessible in the template
            "options" : getOptions,
            "form" : AddOptionForm(),
            **count_data 
            } 
        return render(request, "manager/add_option.html", show)
    
    # @method_decorator(login_required)
    def post(self, request):
        form = AddOptionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("add_option")
        print(form.errors)
        return render(request, "manager/add_option.html", {"form": form})
    
    # def put(self, request, option_id, price) using with javascript

class DeleteOptionView(View):
    # @method_decorator(login_required)
    def get(self, request, option_id):
        getOption = Service.objects.get(pk=option_id)
        getOption.delete()
        return redirect("add_option")
