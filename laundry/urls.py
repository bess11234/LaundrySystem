from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.Index.as_view(), name="index"),

    # show data
    path("manager/report/", views.ReportView.as_view(), name="report"),
    path("manager/addstaff/", views.AddStaffView.as_view(), name="add_staff"),
    path("manager/addmachine/", views.AddMachineView.as_view(), name="add_machine"),
    path("manager/addsize/", views.AddSizeView.as_view(), name="add_size"),
    path("manager/addoption/", views.AddOptionView.as_view(), name="add_option"),

    #delete data
    path("manager/delete/machine/<int:machine_id>", views.DeleteMachineView.as_view(), name="delete_machine"),
    path("manager/delete/size/<int:size_id>", views.DeleteSizeView.as_view(), name="delete_size"),
    path("manager/delete/option/<int:option_id>", views.DeleteOptionView.as_view(), name="delete_option")
]
