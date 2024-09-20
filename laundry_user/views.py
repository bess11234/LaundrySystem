from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.shortcuts import render, redirect

from django.views import View

from laundry_model.models import Users
from .forms import RegisterForm

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
        
class ProfileView(View):
    @method_decorator(login_required)
    def get(self, request):
        profile = Users.objects.get(email=request.user)
        
        return render(request, "profile.html")