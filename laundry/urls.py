from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.Index.as_view(), name="index"),
    # Staff
    path("staff/reserve/", views.ManageReserve.as_view(), name="manage_reserve"),

    # Manager
    ## show data
    path("manager/report/", views.ReportView.as_view(), name="report"),
    path("manager/addstaff/", views.AddStaffView.as_view(), name="add_staff"),
    path("manager/addmachine/", views.AddMachineView.as_view(), name="add_machine"),
    path("manager/addsize/", views.AddSizeView.as_view(), name="add_size"),
    path("manager/addoption/", views.AddOptionView.as_view(), name="add_option"),
]
