from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.Index.as_view(), name="index"),
    path("user/", include("django.contrib.auth.urls")),
    path("user/register/", views.RegisterView.as_view(), name="register"),
    path("user/logout1/", views.user_logout, name="logout1"),
    path("manager/report/", views.ReportView.as_view(), name="report"),
    path("manager/addsize/", views.AddMachineView.as_view(), name="addmachine"),
    path("manager/addsize/", views.AddSizeView.as_view(), name="addsize")
]
