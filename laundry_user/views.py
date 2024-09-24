from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.shortcuts import render, redirect

from django.views import View

from laundry_model.models import Users
from .forms import RegisterForm, ProfileForm

from django.contrib.auth.mixins import LoginRequiredMixin

class RegisterView(View):
    def get(self, request):
        if (request.user.is_authenticated):
            return redirect("index")
        form = RegisterForm()
        return render(request, "register.html", {
            "form": form
        })
    
    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("index") # กลับไปหน้าหลัก มีการ Setting.py อยู่แล้วจึงไม่จำเป็นต้อง Redirect อีก
        return render(request, "register.html", {
            "form": form
        })
        
class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        profile = Users.objects.get(email=request.user)
        form = ProfileForm(instance=profile)
        return render(request, "profile.html", {"form": form, "sidebar": "sidebar_item/profile.html"})
    
    def post(self, request):
        profile = Users.objects.get(email=request.user)
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid() and request.user.email == request.POST.get("email") and request.user.phone == request.POST.get("phone"):
            form.save()
            return redirect("profile")
        return render(request, "profile.html", {"form": form, "sidebar": "sidebar_item/profile.html"})