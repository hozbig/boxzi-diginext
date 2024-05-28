from django import forms

from .models import Topic

class TopicSubjectCreationForm(forms.Form):
    topic_name = forms.CharField(max_length=255, required=False, label="موضوع جدید")
    topic = forms.ModelChoiceField(queryset=Topic.objects.all(), required=False, label="موضوع انتخابی")
    subject_name = forms.CharField(max_length=255, label="زیر موضوع")
