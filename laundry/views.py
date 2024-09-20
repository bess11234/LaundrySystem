from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect
from django.views import View
from laundry_model.models import *
# Create your views here.

class Index(View):
    def get(self, request):
        return render(request, "index.html")
# Customer

# Staff

# Manager
class ReportView(View):
    @login_required
    def get(self, request):
        return render(request, "manager/report.html")
    
class AddMachineView(View):
    @login_required
    def get(self, request):
        return render(request, "manager/addmachine.html")
    
class AddSizeView(View):
    @login_required
    def get(self, request):
        getSize = Machine_Size.objects.all().order_by("capacity")
        for size in getSize:
            print(size.size)
        show = {"sizes": getSize}
        return render(request, "manager/addsize.html", show)