from django import forms
from laundry_model.models import *
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django.forms.widgets  import Select

import string

# Customer
class ReserveMachineForm(ModelForm):
    class Meta:
        model = Reserve_Machine
        fields = [
            "machine_size",
            "arrive_at",
            "service"
        ]

# Manager
myclass = "mt-2 w-full rounded-lg shadow-sm bg-[#f9fbfc] dark:bg-[#353a55] border border-gray-300 dark:border-gray-600 focus:border-[#4c569b] focus:ring-1 focus:ring-[#4c569b] py-2 px-3 text-gray-900 dark:text-white transition read-only:border-opacity-50 read-only:bg-opacity-50 read-only:text-opacity-70"
class AddSizeForm(ModelForm):
    class Meta:
        model = Machine_Size
        fields = [
            "size", 
            "capacity",
            "cost"
        ]
        
class AddOptionForm(ModelForm):
    class Meta:
        model = Service
        fields = "__all__"


class AddMachineForm(ModelForm):
    code = forms.CharField(widget=forms.TextInput(attrs={"class": myclass, "placeholder": "X-XXXXXXXX"}), min_length=3,max_length=10, help_text="ex.'A-0', 'A-1', ..., 'B-0'")
    machine_size = forms.ModelChoiceField(
        queryset=Machine_Size.objects.order_by("capacity"),
        widget=forms.Select(attrs={"class": "mt-2 w-full rounded-lg shadow-md bg-[#f9fbfc] dark:bg-[#353a55] border border-gray-300 dark:border-gray-600 focus:border-[#4c569b] focus:ring-2 focus:ring-[#4c569b] py-2 px-3 text-gray-900 dark:text-white transition ease-in-out duration-150 appearance-none cursor-pointer"}))
    duration = forms.IntegerField(widget=forms.NumberInput(attrs={"class":myclass, "placeholder": "Operation time (Minutes)"}), min_value=0)
    class Meta:
        model = Machine
        fields = [
                "machine_size", 
                "code",
                "duration"]
    
    def clean_code(self):
        code = self.cleaned_data.get("code")
        try:
            if not (code[0] in string.ascii_uppercase and code[1] == "-" and int(code[2:]) >= 0):
                raise ValidationError(
                    "Ensure that format be like 'A-0', 'A-1', .."
                )
        except ValueError:
            raise ValidationError(
                "Ensure that format be like 'A-0', 'A-1', .."
            )
        return code

class AddStaffForm(ModelForm):
    class Meta:
        model = Users
        fields = [
            "status",
            "role"
        ]
        # widgets = {
        #     "role": Select(attrs={"class": "block w-full rounded-md py-2 px-2 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"})
        # }
