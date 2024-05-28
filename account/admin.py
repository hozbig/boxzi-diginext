from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Meeting, WorkExperience, LeanCanvas
from .forms import CustomUserCreationForm


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    model = User
    list_display = [
        "username",
        "first_name",
        "last_name",
        "is_team_member",
        "is_investor",
        "is_company_staff",
        "is_center_staff",
        "is_mentor",
        "is_staff",
        "is_superuser",
        "type",
    ]
    add_fieldsets = (
        (
            "اطلاعات احراز هویت",
            {
                "fields": (
                    "username",
                    "password1",
                    "password2",
                )
            },
        ),
        (
            "نقش کاربر؟",
            {
                "fields": (
                    "is_mentor",
                    "is_team_member",
                    "is_investor",
                    "access_to_company",
                    "access_to_center",
                )
            },
        )
    )
    fieldsets = UserAdmin.fieldsets + (
        (
            "مشخصات اضافی کاربر هدف",
            {
                "fields": (
                    "type",
                    "birthday",
                    "major",
                    "number_id",
                    "phone_number",
                    "interests",
                    "abilities",
                    "bio",
                )
            },
        ),
    )
    fieldsets[2][1]["fields"] = (
        "is_active",
        "is_team_member",
        "is_investor",
        "is_mentor",
        "is_staff",
        "is_superuser",
        # "groups",
        # "user_permissions",
        "access_to_company",
        "access_to_center",
        "received_medals",
    ),
    filter_horizontal = (
        "groups",
        "user_permissions",
        "interests",
        "abilities",
        "access_to_company",
    )
    autocomplete_fields = ("access_to_center",)
    list_filter = ("is_staff", "is_superuser", "is_active", "groups", "is_mentor", "is_team_member", "is_investor", "interests", "abilities", "type")
    # readonly_fields = ("received_medals",)

admin.site.register(User, CustomUserAdmin)


class MeetingAdmin(admin.ModelAdmin):
    list_display = [
        "team",
        "team_member",
        "mentor",
        "date",
        "time",
        "topic",
        "description",
        "status",
        "rate",
    ]
    list_filter = [
        "team",
        "mentor",
        "date",
        "status",
        "rate",
        "created_time",
        "last_update_time",
    ]
    search_fields = ["topic"]
    readonly_fields = [
        "team",
        "team_member",
        "mentor",
        "date",
        "time",
        "topic",
        "description",
        "status",
        "rate",
    ]

admin.site.register(Meeting, MeetingAdmin)


class WorkExperienceAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "topic",
        "from_date",
        "to_date",
        "type",
        "description",
        "uuid",
    ]
    list_filter = [
        "user",
        "type",
        "created_time",
        "last_update_time",
    ]
    search_fields = ["topic", ]

admin.site.register(WorkExperience, WorkExperienceAdmin)


class LeanCanvasAdmin(admin.ModelAdmin):
    list_display = [
        "data",
    ]
    list_filter = [
        "created_time",
        "last_update_time",
    ]

admin.site.register(LeanCanvas, LeanCanvasAdmin)