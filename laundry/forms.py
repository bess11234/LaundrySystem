from django import forms
from laundry_model.models import *
from django.forms import ModelForm

class AddSizeForm(ModelForm):
    class Meta:
        model = Machine_Size
        fields = [
            "size", 
            "capacity"]
        
class AddOptionForm(ModelForm):
    class Meta:
        model = Service
        fields = "__all__"
