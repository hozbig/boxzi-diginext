from django.contrib import admin

from .models import Exam, Answer, Question, UserExamAnsewrHistory, ExamOrder, PreRegisterTask, PersonalTest

admin.site.register(PersonalTest)
admin.site.register(PreRegisterTask)
admin.site.register(ExamOrder)
class ExamAdmin(admin.ModelAdmin):
    list_display = ["name", "medals", "uuid"]
    list_filter = ["created_time", "last_update_time"]
    search_fields = ["name", "questions", "medals"]


admin.site.register(Exam, ExamAdmin)


class AnswerAdmin(admin.ModelAdmin):
    list_display = ["text", "is_valid"]
    list_filter = ["is_valid", "created_time", "last_update_time"]
    search_fields = ["text"]


admin.site.register(Answer, AnswerAdmin)


class QuestionAdmin(admin.ModelAdmin):
    list_display = ["text"]
    list_filter = ["created_time", "last_update_time"]
    search_fields = ["text", "answers__text"]
    filter_horizontal = ["answers"]


admin.site.register(Question, QuestionAdmin)


class UserExamAnsewrHistoryAdmin(admin.ModelAdmin):
    list_display = ["user", "exam", "question", "answer"]
    search_fields = ["user__username", "exam__name", "question__text", "answer__text"]
    list_filter = ["user", "created_time", "last_update_time"]
    readonly_fields = ["user", "exam", "question", "answer"]

admin.site.register(UserExamAnsewrHistory, UserExamAnsewrHistoryAdmin)
