from django.forms import ModelForm

from .models import RoadRegistration, StartUpTeam, TeamMember


class RoadRegistrationForm(ModelForm):
    class Meta:
        model = RoadRegistration
        exclude = ("created_time", "last_update_time", "uuid")


class StartUpTeamForm(ModelForm):
    class Meta:
        model = StartUpTeam
        exclude = ("created_time", "last_update_time", "uuid", "team_members", "team_mentors")


class TeamMemberForm(ModelForm):
    class Meta:
        model = TeamMember
        exclude = ("created_time", "last_update_time", "uuid", "is_owner", "user", "user_validation_code")
