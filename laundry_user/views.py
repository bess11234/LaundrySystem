from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.views import View

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