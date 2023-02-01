from django.contrib import admin
from django.contrib.admin import ModelAdmin

from users.models import Lid, LidIncrement


@admin.register(Lid)
class LidAdmin(ModelAdmin):
    pass


@admin.register(LidIncrement)
class LidIncrementAdmin(ModelAdmin):
    pass
