from django.contrib import admin
from django.contrib.admin import ModelAdmin

from apps.models import Role, Branch
from users.models import User


@admin.register(User)
class UserAdmin(ModelAdmin):
    pass


@admin.register(Role)
class RoleAdmin(ModelAdmin):
    pass


@admin.register(Branch)
class BranchAdmin(ModelAdmin):
    pass
