from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.auth import models

from apps.groups.models import Role, Branch, Group, Course
from apps.users.models import User
from apps.groups.models import Room

admin.site.unregister(models.Group)


@admin.register(Group)
class GroupAdmin(ModelAdmin):
    list_filter = 'name',


@admin.register(Room)
class RoomAdmin(ModelAdmin):
    list_filter = 'name', 'branch'


@admin.register(Course)
class CourseAdmin(ModelAdmin):
    pass


@admin.register(User)
class UserAdmin(ModelAdmin):
    pass


@admin.register(Role)
class RoleAdmin(ModelAdmin):
    pass


@admin.register(Branch)
class BranchAdmin(ModelAdmin):
    pass
