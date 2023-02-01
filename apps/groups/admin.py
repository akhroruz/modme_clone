from django.contrib import admin
from django.contrib.admin import ModelAdmin

from groups.models import Room, Branch, CourseGroup, Course
from users.models import User


@admin.register(CourseGroup)
class CourseGroupAdmin(ModelAdmin):
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
