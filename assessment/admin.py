from django.contrib import admin

from . import models


class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "key_name", "count_of_questions"]

admin.site.register(models.Category, CategoryAdmin)


class ResponseAdmin(admin.ModelAdmin):
    list_display = [
        "question",
        "referee",
        "point",
        "plan",
        "team",
        "individual",
        "personal_test",
        "pre_register_change",
    ]

admin.site.register(models.Response, ResponseAdmin)


class QuestionAdmin(admin.ModelAdmin):
    list_display = ["question", "category"]
    
admin.site.register(models.Question, QuestionAdmin)
