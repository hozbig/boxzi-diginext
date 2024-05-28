from django.forms import ModelForm
from django.forms import Textarea

from .models import Plan


class PlanCreateForm(ModelForm):
    class Meta:
        model = Plan
        exclude = ("created_time", "last_update_time", "likes")
        widgets = {
            'description': Textarea(attrs={'style': 'height: 150px;'}),
        }