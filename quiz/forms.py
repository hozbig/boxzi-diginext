from django.forms import ModelForm
from django_quill.forms import QuillFormField

from .models import (
    Exam, 
    Question, 
    Answer, 
    ExamOrder, 
    Task,
    TaskOrder,
    PreRegisterTask,
    PreRegisterTaskResponse,
    )


class ExamCreateForm(ModelForm):
    class Meta:
        model = Exam
        exclude = ("created_time", "last_update_time", "questions")


class ExamUpdateForm(ModelForm):
    class Meta:
        model = Exam
        exclude = ("created_time", "last_update_time", "uuid", "accelerator", "questions")


class TaskCreateForm(ModelForm):
    class Meta:
        model = Task
        text = QuillFormField()
        exclude = ("created_time", "last_update_time")


class TaskUpdateForm(ModelForm):
    class Meta:
        model = Task
        text = QuillFormField()
        exclude = ("created_time", "last_update_time", "accelerator")
        
        
class TaskOrderForm(ModelForm):
    class Meta:
        model = TaskOrder
        exclude = ("created_time", "last_update_time")
        
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(TaskOrderForm, self).__init__(*args, **kwargs)
        self.fields['task'].queryset = Task.objects.filter(accelerator=user.access_to_center)


class QuestionCreateForm(ModelForm):
    class Meta:
        model = Question
        exclude = ("created_time", "last_update_time", "answers")


class AnswerCreateForm(ModelForm):
    class Meta:
        model = Answer
        exclude = ("created_time", "last_update_time")


class ExamOrderCreateForm(ModelForm):
    class Meta:
        model = ExamOrder
        exclude = ("created_time", "last_update_time")

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(ExamOrderCreateForm, self).__init__(*args, **kwargs)
        self.fields['exam'].queryset = Exam.objects.filter(accelerator=user.access_to_center)


class PreRegisterTaskCreateForm(ModelForm):
    class Meta:
        model = PreRegisterTask
        text = QuillFormField()
        exclude = ("created_time", "last_update_time")
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["start_date"].widget.attrs['class'] = "flatpickr-date"
        self.fields["expiration_date"].widget.attrs['class'] = "flatpickr-date"
        
        
class PreRegisterTaskUpdateForm(ModelForm):
    class Meta:
        model = PreRegisterTask
        text = QuillFormField()
        exclude = ("created_time", "last_update_time", "accelerator")
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["start_date"].widget.attrs['class'] = "flatpickr-date"
        self.fields["expiration_date"].widget.attrs['class'] = "flatpickr-date"
        

class PreRegisterTaskResponseCreateForm(ModelForm):
    class Meta:
        model = PreRegisterTaskResponse
        text = QuillFormField()
        exclude = ("created_time", "last_update_time")


class PreRegisterTaskResponseUpdateForm(ModelForm):
    class Meta:
        model = PreRegisterTaskResponse
        text = QuillFormField()
        exclude = ("created_time", "last_update_time", "uuid", "user", "road", "task")
