from django.forms import ModelForm, ModelMultipleChoiceField
from django_quill.forms import QuillFormField
from quiz.models import Exam

from .models import Road, Collection, Content, CollectionOrder, ContentOrder


class RoadCreateForm(ModelForm):
    class Meta:
        model = Road
        exclude = ("created_time", "last_update_time", "uuid")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            self.fields[field_name].required = True
            if isinstance(field, ModelMultipleChoiceField):
                field.widget.attrs['class'] = 'select2'
        self.fields["poster"].widget.attrs['class'] = "form-control"
        self.fields["start_date"].widget.attrs['class'] = "flatpickr-date"
        self.fields["expiration_date"].widget.attrs['class'] = "flatpickr-date"
        self.fields["publish_date"].widget.attrs['class'] = "flatpickr-date"
        self.fields["registration_deadline"].widget.attrs['class'] = "flatpickr-date"


class RoadUpdateForm(ModelForm):
    class Meta:
        model = Road
        exclude = ("created_time", "last_update_time", "uuid", "accelerator")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            self.fields[field_name].required = True
            if isinstance(field, ModelMultipleChoiceField):
                field.widget.attrs['class'] = 'select2'
        self.fields["poster"].widget.attrs['class'] = "form-control"
        self.fields["start_date"].widget.attrs['class'] = "flatpickr-date"
        self.fields["expiration_date"].widget.attrs['class'] = "flatpickr-date"
        self.fields["publish_date"].widget.attrs['class'] = "flatpickr-date"
        self.fields["registration_deadline"].widget.attrs['class'] = "flatpickr-date"


class CollectionCreateForm(ModelForm):
    class Meta:
        model = Collection
        exclude = ("created_time", "last_update_time", "type", "uuid", "exam")

    def __init__(self, *args, **kwargs):
        super(CollectionCreateForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, ModelMultipleChoiceField):
                field.widget.attrs['class'] = 'select2'


class CollectionOrderCreateForm(ModelForm):
    class Meta:
        model = CollectionOrder
        exclude = ("created_time", "last_update_time")

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(CollectionOrderCreateForm, self).__init__(*args, **kwargs)
        self.fields['collection'].queryset = Collection.objects.filter(accelerator=user.access_to_center)


class CollectionUpdateForm(ModelForm):
    class Meta:
        model = Collection
        exclude = ("created_time", "last_update_time", "type", "uuid", "accelerator", "exam")

    def __init__(self, *args, **kwargs):
        super(CollectionUpdateForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, ModelMultipleChoiceField):
                field.widget.attrs['class'] = 'select2'


class ContentCreateForm(ModelForm):
    class Meta:
        model = Content
        content = QuillFormField()
        exclude = ("created_time", "last_update_time", "uuid")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, ModelMultipleChoiceField):
                field.widget.attrs['class'] = 'select2'


class ContentUpdateForm(ContentCreateForm):
    class Meta:
        model = Content
        exclude = ("created_time", "last_update_time", "uuid", "accelerator")


class ContentOrderCreateForm(ModelForm):
    class Meta:
        model = ContentOrder
        exclude = ("created_time", "last_update_time")

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(ContentOrderCreateForm, self).__init__(*args, **kwargs)
        self.fields['content'].queryset = Content.objects.filter(accelerator=user.access_to_center)
