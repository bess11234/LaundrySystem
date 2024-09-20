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
        getSize = Machine_Size.objects.all().order_by("capacity") # get size for show in table
        for size in getSize:
            print(size.size)
        show = {"sizes": getSize, 
                "form" : AddSizeForm()}
        return render(request, "manager/add_size.html", show)
    
    def post(self, request):
        form = AddSizeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add_size') #refresh page for show new inserted data
        form.errors()
        return render(request, "project_form.html", {"form": form}) #stay in same page

    # Delete Size
class DeleteSizeView(View):
    def get(self, request, size_id):
        get_size = Machine_Size.objects.get(pk=size_id)
        get_size.delete()
        return redirect("add_size")
    
    # Option
class AddOptionView(View):
    def get(self, request):
        return render(request, "manager/add_option.html")