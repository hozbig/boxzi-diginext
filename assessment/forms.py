from django.forms import ModelForm
from .models import Question


class QuestionCreateForm(ModelForm):
    class Meta:
        model = Question
        exclude = ("created_time", "last_update_time")
