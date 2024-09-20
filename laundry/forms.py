from django import forms
from laundry_model.models import *
from django.forms import ModelForm

class AddSizeForm(ModelForm):
    class Meta:
        model = Machine_Size
        fields = [
            "size", 
            "capacity"]
        
# class RegisterForm(UserCreationForm):
#     class Meta:
#         model = Users
#         fields = ["email", "first_name", "last_name", "phone"]
    
#     phone = forms.CharField(max_length=10, min_length=10)
    
#     def clean_phone(self):
#         phone = self.cleaned_data.get("phone")
#         if phone[2] not in ("02","06","08","09"):
#             raise ValidationError(
#                 "Phone should start with '02', '06', '08', '09'"
#             )
#         return phone
