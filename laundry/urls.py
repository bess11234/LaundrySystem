from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.Index.as_view(), name="index"),
    # Customer
    path("reserve/", views.ReserveMachineView.as_view(), name="reserve_machine"),
    path("customer/view_reserve/", views.ViewReserve.as_view(), name="view_reserve"),
    
    # Staff
    path("staff/reserve/", views.ManageReserve.as_view(), name="manage_reserve"),

    # Manager
    ## show data
    path("report/", views.ReportView.as_view(), name="report"),
    path("manager/addstaff/", views.AddStaffView.as_view(), name="add_staff"),
    path("manager/addmachine/", views.AddMachineView.as_view(), name="add_machine"),
    path("manager/addsize/", views.AddSizeView.as_view(), name="add_size"),
    path("manager/addoption/", views.AddOptionView.as_view(), name="add_option"),

    ## Test
    path("test/", views.TestView.as_view(), name="test"),
]
