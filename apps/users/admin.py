from django.contrib import admin
from django.contrib.admin import ModelAdmin

from users.models import Lead, LeadIncrement, User


@admin.register(Lead)
class LeadAdmin(ModelAdmin):
    pass


@admin.register(LeadIncrement)
class LeadIncrementAdmin(ModelAdmin):
    pass


@admin.register(User)
class UserAdmin(ModelAdmin):
    exclude = ('group', 'last_login', 'date_joined', 'deleted_at')
