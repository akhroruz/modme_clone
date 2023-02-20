from django.contrib import admin
from django.contrib.admin import ModelAdmin
from groups.models import Room, Branch, Group, Course, Company


@admin.register(Group)
class GroupAdmin(ModelAdmin):
    list_display = ('branch', 'teacher_name', 'course', 'status')

    def teacher_name(self, obj: Group):  # noqa
        return obj.teacher.first_name


@admin.register(Room)
class RoomAdmin(ModelAdmin):
    list_display = ('name', 'branch')


@admin.register(Course)
class CourseAdmin(ModelAdmin):
    list_display = ('name', 'company', 'price', 'image')


@admin.register(Branch)
class BranchAdmin(ModelAdmin):
    list_display = ('name', 'company', 'phone', 'address', 'image')


@admin.register(Company)
class CompanyAdmin(ModelAdmin):
    pass
