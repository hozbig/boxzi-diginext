from django.contrib import admin, messages

from .andaze import get_user_data

from .models import (
    Exam,
    Answer,
    Question,
    UserExamAnsewrHistory,
    ExamOrder,
    PreRegisterTask,
    PreRegisterTaskQuestion,
    PreRegisterTaskResponse,
    PersonalTest
)

admin.site.register(PreRegisterTask)
admin.site.register(PreRegisterTaskQuestion)
admin.site.register(PreRegisterTaskResponse)
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


class PersonalTestAdmin(admin.ModelAdmin):
    list_display = ["user", "reference_id", "first_response_of_sending_information_is_accepted", "final_user_result_url"]
    actions = ("get_user_test_result", "null_result")

    @admin.action(description='دریافت نتیجه آزمون کاربر')
    def get_user_test_result(modeladmin, request, queryset):
        for obj in queryset:
            res = get_user_data(obj.user)
            obj.final_user_result_url = res
            obj.save()
        messages.success(request, "دستور با موفقیت اجرا شد!")

    @admin.action(description='ریست کردن نتیجه های دریافتی')
    def null_result(modeladmin, request, queryset):
        for obj in queryset:
            obj.final_user_result_url = None
            obj.save()
        messages.success(request, "دستور با موفقیت اجرا شد!")


admin.site.register(PersonalTest, PersonalTestAdmin)
