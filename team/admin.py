from django.contrib import admin
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
    autocomplete_fields = ['category',]
    filter_horizontal = ["team_members", "team_mentors"]
    inlines = (PlanInline,)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ["name"]


@admin.register(RoadRegistration)
class RoadRegistrationAdmin(admin.ModelAdmin):
    pass


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ["team", "user", "user_number_id", "is_coordinator", "is_owner"]
    list_filter = ["team", "is_coordinator", "is_owner"]
    search_fields = ["user", "team"]
