from django.forms import ModelForm
from django.forms import Textarea

from .models import Plan


class PlanCreateForm(ModelForm):
    class Meta:
        model = Plan
        exclude = ("created_time", "last_update_time", "likes")

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].label = ""