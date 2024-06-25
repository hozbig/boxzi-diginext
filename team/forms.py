from django import forms
from django.core.validators import RegexValidator

from .models import RoadRegistration, StartUpTeam, TeamMember


class RoadRegistrationForm(forms.ModelForm):
    class Meta:
        model = RoadRegistration
        exclude = ("created_time", "last_update_time", "uuid")


class StartUpTeamForm(forms.ModelForm):
    class Meta:
        model = StartUpTeam
        exclude = ("created_time", "last_update_time", "uuid", "team_members", "team_mentors")


class TeamMemberForm(forms.Form):
    phone_number = forms.CharField(
        max_length=11,
        validators=[
            RegexValidator(
                r'^09\d{9}$',
                message='شماره تماس باید با 09 شروع شده و شامل 11 رقم باشد.'
            )
        ], required=True, label="شماره همراه"
    )
    email = forms.EmailField(required=True, label="ایمیل")
    first_name = forms.CharField(max_length=30, required=True, label="نام")
    last_name = forms.CharField(max_length=30, required=True, label="نام خانوادگی")

    # 'phoneInput' class name related to a js script that exist under the pages that have a html input for phone number
    # Its prevent that user use persian number, its only accept latin number
    phone_number.widget.attrs["class"] = "phoneInput"


class ExtraDaysForCompleteRegistration(forms.Form):
    extra_days = forms.IntegerField(
        label='تعداد روز های اضافی',
        required=True,
        min_value=1,
        error_messages={
            'required': 'پر کردن این فیلد لازم است',
            'min_value': 'مقدار روز وارد شده باید حداقل ۱ باشد'
        }
    )
    registration_object_uuid = forms.CharField(
        required=True,
        max_length=10,
        error_messages={
            'required': 'پر کردن این فیلد لازم است',
            'max_length': 'مقدار وارد شده بیش از طولانی میباشد'
        }
    )
