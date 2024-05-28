from django.forms import ModelForm

from .models import InvestorFound


class InvestorFoundCreationForm(ModelForm):
    class Meta:
        model = InvestorFound
        exclude = ("created_time", "last_update_time", "uuid")


class InvestorFoundUpdateForm(ModelForm):
    class Meta:
        model = InvestorFound
        exclude = ("created_time", "last_update_time", "uuid", "investor")
