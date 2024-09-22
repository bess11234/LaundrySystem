from django.contrib.auth.forms import UserCreationForm
from django import forms

from laundry_model.models import Users

from django.core.exceptions import ValidationError

class RegisterForm(UserCreationForm):
    class Meta:
        model = Users
        fields = ["email", "first_name", "last_name", "phone"]
    
    phone = forms.CharField(max_length=10, min_length=10)
    
    def clean_phone(self):
        phone = self.cleaned_data.get("phone")
        if phone[:2] not in ("02","06","08","09"): 
            raise ValidationError(
                "Phone should start with '02', '06', '08', '09'"
            )
        
        try:
            int(phone)
        except ValueError:
            raise ValidationError(
                "Phone need to be number"
            )
        return phone
    
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Users
        fields = [
            "email",
            "first_name",
            "last_name",
            "phone"
        ]
    email = forms.EmailField(disabled=True)
    phone = forms.CharField(disabled=True)
    phone = forms.CharField(max_length=10, min_length=10)