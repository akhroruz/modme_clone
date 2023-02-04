from django.contrib import admin
from django.contrib.admin import ModelAdmin

from users.models import Lid, LidIncrement, Blog


@admin.register(Lid)
class LidAdmin(ModelAdmin):
    pass


@admin.register(LidIncrement)
class LidIncrementAdmin(ModelAdmin):
    pass


@admin.register(Blog)
class BlogAdmin(ModelAdmin):
    pass
