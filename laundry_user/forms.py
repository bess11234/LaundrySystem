from django.contrib.auth.forms import UserCreationForm
from django import forms

from laundry_model.models import Users

class RegisterForm(UserCreationForm):
    class Meta:
        model = Users
        fields = ["email", "first_name", "last_name", "phone"]
    
    phone = forms.CharField(max_length=10, min_length=10)