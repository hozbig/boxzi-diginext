from django.contrib import admin, messages
from plan.models import Plan

from .models import Category, StartUpTeam, RoadRegistration, TeamMember


class PlanInline(admin.StackedInline):
    model = Plan
    extra = 1
    autocomplete_fields = ['team']


@admin.register(StartUpTeam)
class StartUpTeamAdmin(admin.ModelAdmin):
    list_display = ["name", "status", "team_member_count", "description", "category"]
    list_filter = ["status", "category", "created_time", "last_update_time"]
    search_fields = ["name"]
    inlines = (PlanInline,)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ["name"]


@admin.register(RoadRegistration)
class RoadRegistrationAdmin(admin.ModelAdmin):
    list_display = [
        "user_phone_number",
        "user",
        "team",
        "team_or_individual",
        "complete_registration_date",
        "validity_pride_days",
        "validity_pride_days_for_challenge",
    ]
    list_filter = ["status_user_state", "team", "status",]
    actions = (
        "plus_3_day_to_challenge_validity_period_days",
        "only_3_day_to_challenge_validity_period_days",
    )

    def user_phone_number(self, obj):
        return obj.user.phone_number
    user_phone_number.short_description = "شماره تماس"
    
    @admin.action(description='اضافه کردن 3 روز به مهلت انجام چالش')
    def plus_3_day_to_challenge_validity_period_days(modeladmin, request, queryset):
        for obj in queryset:
            if obj.complete_registration_date:
                obj.validity_pride_days_for_challenge += 3
                obj.save()
        messages.success(request, "دستور با موفقیت اجرا شد!")
        
    @admin.action(description='فقط ۳ روز زمان برای انجام چالش')
    def only_3_day_to_challenge_validity_period_days(modeladmin, request, queryset):
        for obj in queryset:
            obj.validity_pride_days_for_challenge = 3
            obj.save()
        messages.success(request, "دستور با موفقیت اجرا شد!")


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ["team", "user", "is_coordinator", "is_owner"]
    list_filter = ["team", "is_coordinator", "is_owner"]
    search_fields = ["user", "team"]
