from django.contrib.auth import login, logout

from django.shortcuts import render, redirect
from django.views import View

from .forms import RegisterForm
# Create your views here.

class Index(View):
    def get(self, request):
        return render(request, "index.html")

class RegisterView(View):
    def get(self, request):
        return render(request, "register.html", {
            "form": RegisterForm()
        })
    
    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return render(request, "index.html") # กลับไปหน้าหลัก
        return render(request, "register.html", {
            "form": form
        })

def user_logout(request):
    logout(request)
    return redirect("index")

class ReportView(View):
    def get(self, request):
        return render(request, "manager/report.html")
    
class AddMachineView(View):
    def get(self, request):
        return render(request, "manager/addmachine.html")
    
class AddSizeView(View):
    def get(self, request):
        return render(request, "manager/addsize.html")