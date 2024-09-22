from django import forms
from laundry_model.models import *
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django.forms.widgets  import Select

class AddSizeForm(ModelForm):
    class Meta:
        model = Machine_Size
        fields = [
            "size",
            "cost",
            "capacity"]
        
class AddOptionForm(ModelForm):
    class Meta:
        model = Service
        fields = "__all__"


class AddMachineForm(ModelForm):
    code = forms.CharField(widget=forms.TextInput(attrs={"class": "block w-full rounded-md border-0 py-1.5 px-3 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"}))
    machine_size = forms.ModelChoiceField(queryset=Machine_Size.objects.all(), widget=forms.Select(attrs={"class": "block w-full rounded-md py-2 px-2 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"}))
    duration = forms.IntegerField(widget=forms.NumberInput(attrs={"class":"block w-full rounded-md border-0 py-1.5 px-3 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"}))
    
    class Meta:
        model = Machine
        fields = [
                "machine_size", 
                "code",
                "duration"]

class AddStaffForm(ModelForm):
    class Meta:
        model = Users
        fields = [
            "status",
            "role"
        ]
        widgets = {
            "role": Select(attrs={"class": "block w-full rounded-md py-2 px-2 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"})
        }
