from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.Index.as_view(), name="index"),
    path("manager/report/", views.ReportView.as_view(), name="report"),
    path("manager/addsize/", views.AddMachineView.as_view(), name="addmachine"),
    path("manager/addsize/", views.AddSizeView.as_view(), name="addsize")
]
