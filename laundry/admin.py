from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from laundry_model.models import Users

admin.site.register(Users, UserAdmin)