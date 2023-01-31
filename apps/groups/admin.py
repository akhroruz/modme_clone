from django.contrib import admin
from django.contrib.admin import ModelAdmin

from apps.groups.models import Room, Branch, Group, Course
from apps.users.models import User


@admin.register(Group)
class GroupAdmin(ModelAdmin):
    pass


@admin.register(Room)
class RoomAdmin(ModelAdmin):
    pass


@admin.register(Course)
class CourseAdmin(ModelAdmin):
    pass


@admin.register(User)
class UserAdmin(ModelAdmin):
    pass


@admin.register(Branch)
class BranchAdmin(ModelAdmin):
    pass
