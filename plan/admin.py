from django.contrib import admin

from .models import Plan


@admin.register(Plan)
class PlnaAdmin(admin.ModelAdmin):
    pass
