from django.contrib.auth import login, logout

from django.shortcuts import render, redirect
from django.views import View

# Create your views here.

class Index(View):
    def get(self, request):
        return render(request, "index.html")
