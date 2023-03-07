from django.contrib import admin
from django.contrib.admin import ModelAdmin
from users.models import Lead, LeadIncrement, User, Blog


@admin.register(Lead)
class LeadAdmin(ModelAdmin):
    list_display = ('full_name', 'phone', 'status', 'lead_increment')


@admin.register(LeadIncrement)
class LeadIncrementAdmin(ModelAdmin):
    pass


@admin.register(User)
class UserAdmin(ModelAdmin):
    list_display = ('first_name', 'gender', 'photo', 'branches', 'roles')
    exclude = ('group', 'last_login', 'date_joined')

    def branches(self, obj: User):  # noqa
        return ",".join([b.name for b in obj.branch.all()])

    def roles(self, obj: User):  # noqa
        return ",".join([b.name for b in obj.role.all()])


@admin.register(Blog)
class BlogAdmin(ModelAdmin):
    list_display = ('company', 'created_by', 'visible_all', 'view_count')
    exclude = ('view_count',)
