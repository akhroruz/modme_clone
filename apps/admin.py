from django.contrib import admin
from django.contrib.admin import ModelAdmin

from apps.models import User, Role, Branch


# @admin.register(User)
# class UserModelAdmin(ModelAdmin):
#     list_display = ['id', 'full_name', 'role']
#
#
# @admin.register(Role)
# class RoleModelAdmin(ModelAdmin):
#     list_display = ['id', 'name']
#
#
# @admin.register(Branch)
# class BranchModelAdmin(ModelAdmin):
#     list_display = ['id', 'phone_number']
