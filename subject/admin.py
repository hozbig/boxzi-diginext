from django.contrib import admin
from .models import Subject, Topic


class AdminTopic(admin.ModelAdmin):
    search_fields = ["name"]


admin.site.register(Topic, AdminTopic)


class SubjectAdmin(admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]
    autocomplete_fields = ["topic"]


admin.site.register(Subject, SubjectAdmin)