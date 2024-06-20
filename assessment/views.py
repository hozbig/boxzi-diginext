from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy

from .forms import QuestionCreateForm
from .models import Question


class CreateQuestion(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Question
    form_class = QuestionCreateForm
    template_name = "assessment/question/create.html"
    success_message = "عملیات با موفقیت انجام شد"
    success_url = reverse_lazy("assessment:create-question")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "مدیریت سوال های داوری"
        context["object_list"] = self.model.objects.all()
        return context    
