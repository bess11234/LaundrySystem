from django.contrib.auth import login, logout

from django.shortcuts import render, redirect
from django.views import View

#import model form laundry_model app
from laundry_model.models import *

# import form
from laundry.forms import *

class Index(View):
    def get(self, request):
        return render(request, "index.html")

# Manager Page

# count all data (use in sidebar)
def count_all_data():
    count_data = {
        "count_staff": Users.objects.filter(role="staff").count(),
        "count_machine": Machine.objects.count(),
        "count_size": Machine_Size.objects.count(),
        "count_service": Service.objects.count()
        }
    return count_data

    # Report
class ReportView(View):
    def get(self, request):
        return render(request, "manager/report.html")

    # Machine
class AddMachineView(View):
    def get(self, request):
        return render(request, "manager/add_machine.html")

    # Size
class AddSizeView(View):
    def get(self, request):
        # check order (asc, desc) request
        order = request.GET.get('order', 'desc') # set first click to desc
        if order == "desc":
            getSizes = Machine_Size.objects.all().order_by("-capacity") # order by asc
        else:
            getSizes = Machine_Size.objects.all().order_by("capacity") # order by desc

        count_data = count_all_data()

        show = {"request": request, #request object will be accessible in the temp
                "sizes": getSizes, 
                "form" : AddSizeForm(),
                **count_data
                }
        return render(request, "manager/add_size.html", show)
    
    def post(self, request):
        form = AddSizeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add_size') # refresh page for show new inserted data
        print(form.errors)
        return render(request, "manager/add_size.html", {"form": form}) # stay in same page and still fill data

    # Delete Size
class DeleteSizeView(View):
    def get(self, request, size_id):
        getSize = Machine_Size.objects.get(pk=size_id)
        getSize.delete()
        return redirect("add_size")
    
    # Option
class AddOptionView(View):
    def get(self, request):
        # check order (asc, desc) request
        order = request.GET.get('order', 'desc') # set first click to desc
        if order == 'desc':
            getOptions = Service.objects.all().order_by("-price") # order by asc
        else:
            getOptions = Service.objects.all().order_by("price") # order by desc

        count_data = count_all_data()
        show = {
            "request": request,# request object will be accessible in the template
            "options" : getOptions,
            "form" : AddOptionForm(),
            **count_data 
            } 
        return render(request, "manager/add_option.html", show)
    
    def post(self, request):
        form = AddOptionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("add_option")
        print(form.errors)
        return render(request, "manager/add_option.html", {"form": form})
    
    # def put(self, request, option_id, price) using with javascript

class DeleteOptionView(View):
    def get(self, request, option_id):
        getOption = Service.objects.get(pk=option_id)
        getOption.delete()
        return redirect("add_option")