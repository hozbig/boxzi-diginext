from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, ListView, View, CreateView, UpdateView, DeleteView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from utils import date_db_convertor
from content.models import Content, Collection, Road, CollectionOrder, ContentOrder
from content.forms import (
    RoadCreateForm, 
    RoadUpdateForm, 
    CollectionCreateForm, 
    CollectionUpdateForm, 
    ContentCreateForm, 
    ContentUpdateForm,
    CollectionOrderCreateForm,
    ContentOrderCreateForm,
)
from quiz.models import Exam, Question, Answer, ExamOrder, Task, TaskOrder, PreRegisterTask
from quiz.forms import (
    ExamCreateForm,
    ExamUpdateForm,
    QuestionCreateForm,
    AnswerCreateForm,
    ExamOrderCreateForm,
    TaskCreateForm,
    TaskUpdateForm,
    TaskOrderForm,
    PreRegisterTaskCreateForm,
    PreRegisterTaskUpdateForm,
)
from subject.models import Topic, Subject
from subject.forms import TopicSubjectCreationForm

from .models import Company, Center
from .mixins import CompanyAdminMixin


# ====== Company Views ======
class CompanyList(LoginRequiredMixin, ListView):
    model = Company
    template_name = "company/list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = f"بازارچه" 
        return context


class CompanyProfile(LoginRequiredMixin, DetailView):
    model = Company
    template_name = "company/profile.html"
    slug_field, slug_url_kwarg = "uuid", "uuid"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = f"پروفایل شرکت" 
        return context


class CompanyDashboard(LoginRequiredMixin, CompanyAdminMixin, View): # Access only for company admin
    model = Company
    template_name = "company/dashboard.html"
    context = {}

    def get(self, request):
        try:
            self.context["title"] = ("داشبورد شرکت " + request.user.access_to_company.first().name)
        except:
            pass
        self.context["companies"] = request.user.access_to_company.all()
        return render(request, self.template_name, self.context)


# ====== Center Views ======
class CenterList(LoginRequiredMixin, ListView):
    model = Center
    template_name = "company/center/list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = f"مراکز رشد و شتابدهی" 
        return context


class CenterProfile(LoginRequiredMixin, DetailView):
    model = Center
    template_name = "company/center/profile.html"
    slug_field, slug_url_kwarg = "uuid", "uuid"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = (
            f"پروفایل {self.get_object().get_type_display()}" 
        )
        return context


class AcceleratorDashboard(LoginRequiredMixin, View):
    model = Center
    template_name = "company/center/dashboard.html"
    context = {
        "title": "داشبورد شتابدهنده",
    }

    def get(self, request):
        user = request.user
        self.context["object"] = user.access_to_center
        return render(request, self.template_name, self.context)


class CreateRoad(LoginRequiredMixin, View):
    model = Road
    form_class = RoadCreateForm
    template_name = "company/center/accelerator/new-road.html"
    success_message = "عملیات با موفقیت انجام شد"
    context = {"title": "مدیریت مسیرها"}


    def get(self, request):
        self.context["form"] = self.form_class
        self.context["acc_object"] = self.request.user.access_to_center
        return render(request, self.template_name, self.context)
    
    def post(self, request):
        form_copy = request.POST.copy()
        form_copy.update(
            {
                "start_date": date_db_convertor.jdate_edge_convertor(form_copy["start_date"]),
                "expiration_date": date_db_convertor.jdate_edge_convertor(form_copy["expiration_date"]),
                "publish_date": date_db_convertor.jdate_edge_convertor(form_copy["publish_date"]),
                "registration_deadline": date_db_convertor.jdate_edge_convertor(form_copy["registration_deadline"]),
            }
        )

        form = self.form_class(form_copy, request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request, self.success_message)
        else:
            messages.error(request, "مشکلی در فرم وجود دارد!")
        
        return redirect(reverse('company:new-road'))

    
class UpdateRoad(LoginRequiredMixin, View):
    model = Road
    form_class = RoadUpdateForm
    template_name = "company/center/accelerator/update-road.html"
    success_message = "عملیات با موفقیت انجام شد"
    context = {"title": "ویرایش مسیرها"}


    def get(self, request, uuid):
        obj = self.model.objects.get(uuid=uuid)
        self.context["form"] = self.form_class(instance=obj)
        self.context["collection_order_form"] = CollectionOrderCreateForm(user=request.user)
        self.context["object"] = self.model.objects.get(uuid=uuid)
        self.context["acc_object"] = self.request.user.access_to_center
        return render(request, self.template_name, self.context)
    
    def post(self, request, uuid):
        form_copy = request.POST.copy()
        form_copy.update(
            {
                "start_date": date_db_convertor.jdate_edge_convertor(form_copy["start_date"]),
                "expiration_date": date_db_convertor.jdate_edge_convertor(form_copy["expiration_date"]),
                "publish_date": date_db_convertor.jdate_edge_convertor(form_copy["publish_date"]),
                "registration_deadline": date_db_convertor.jdate_edge_convertor(form_copy["registration_deadline"]),
            }
        )

        obj = self.model.objects.get(uuid=uuid)
        form = self.form_class(form_copy, request.FILES, instance=obj)

        if form.is_valid():
            form.save()
            messages.success(request, self.success_message)
        else:
            messages.error(request, "مشکلی در فرم وجود دارد!")
        
        return redirect(reverse('company:update-road', kwargs={'uuid': uuid}))
    

class DeleteRoad(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Road
    template_name = "company/center/accelerator/confirm-delete.html"
    success_message = "عملیات با موفقیت انجام شد"
    success_url = reverse_lazy('company:new-road')
    slug_field, slug_url_kwarg = "uuid", "uuid"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "حذف مسیر"
        return context
    

@login_required
@require_POST
def save_collection_order(request, road_uuid):
    road_instance = Road.objects.get(uuid=road_uuid)
    if request.method == 'POST':
        form_copy = request.POST.copy()
        form_copy.update({"road": road_instance,})

        form = CollectionOrderCreateForm(form_copy, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "عملیات با موفقیت انجام شد")
        else:
            messages.error(request, "مشکلی در فرم وجود دارد!")
    else:
        messages.error(request, "درخاست نامعتبر!")
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


@login_required
def delete_collection_order(request, pk):
    try:
        CollectionOrder.objects.get(pk=pk).delete()
        messages.success(request, "عملیات با موفقیت انجام شد")
    except:
        messages.error(request, "درخاست نامعتبر!")

    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
    

class CreateCollection(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Collection
    form_class = CollectionCreateForm
    template_name = "company/center/accelerator/new-collection.html"
    success_message = "عملیات با موفقیت انجام شد"
    success_url = reverse_lazy("company:new-collection")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "مدیریت فصل ها"
        context["acc_object"] = self.request.user.access_to_center
        return context


class UpdateCollection(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Collection
    form_class = CollectionUpdateForm
    template_name = "company/center/accelerator/update-collection.html"
    success_message = "عملیات با موفقیت انجام شد"
    slug_field, slug_url_kwarg = "uuid", "uuid"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "ویرایش فصل"
        context["content_order_form"] = ContentOrderCreateForm(user=self.request.user)
        context["exam_order_form"] = ExamOrderCreateForm(user=self.request.user)
        context["task_order_form"] = TaskOrderForm(user=self.request.user)
        return context
    
    def get_success_url(self, **kwargs):         
        return reverse_lazy('company:update-collection', args = (self.object.uuid,))
    

class DeleteCollection(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Collection
    template_name = "company/center/accelerator/confirm-delete.html"
    success_message = "عملیات با موفقیت انجام شد"
    success_url = reverse_lazy('company:new-collection')
    slug_field, slug_url_kwarg = "uuid", "uuid"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "حذف فصل"
        return context


@login_required
@require_POST
def save_content_order(request, collection_uuid):
    collection_instance = Collection.objects.get(uuid=collection_uuid)
    if request.method == 'POST':
        form_copy = request.POST.copy()
        form_copy.update({"collection": collection_instance,})

        form = ContentOrderCreateForm(form_copy, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "عملیات با موفقیت انجام شد")
        else:
            messages.error(request, "مشکلی در فرم وجود دارد!")
    else:
        messages.error(request, "درخاست نامعتبر!")
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


@login_required
def delete_content_order(request, pk):
    try:
        ContentOrder.objects.get(pk=pk).delete()
        messages.success(request, "عملیات با موفقیت انجام شد")
    except:
        messages.error(request, "درخاست نامعتبر!")

    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


class CreateContent(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Content
    form_class = ContentCreateForm
    template_name = "company/center/accelerator/new-content.html"
    success_message = "عملیات با موفقیت انجام شد"
    success_url = reverse_lazy("company:new-content")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "مدیریت گام ها"
        context["acc_object"] = self.request.user.access_to_center
        return context


class UpdateContent(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Content
    form_class = ContentUpdateForm
    template_name = "company/center/accelerator/update-content.html"
    success_message = "عملیات با موفقیت انجام شد"
    slug_field, slug_url_kwarg = "uuid", "uuid"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "ویرایش گام"
        context["acc_object"] = self.request.user.access_to_center
        return context

    def get_success_url(self, **kwargs):         
        return reverse_lazy('company:update-content', args = (self.object.uuid,))
    

class DeleteContent(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Content
    template_name = "company/center/accelerator/confirm-delete.html"
    success_message = "عملیات با موفقیت انجام شد"
    success_url = reverse_lazy('company:new-content')
    slug_field, slug_url_kwarg = "uuid", "uuid"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "حذف گام"
        return context
    

class CreateExam(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Exam
    form_class = ExamCreateForm
    template_name = "company/center/accelerator/new-exam.html"
    success_message = "عملیات با موفقیت انجام شد"
    success_url = reverse_lazy("company:new-exam")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "مدیریت آزمون ها"
        context["acc_object"] = self.request.user.access_to_center
        context["task_form"] = TaskCreateForm
        return context


class UpdateExam(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Exam
    form_class = ExamUpdateForm
    template_name = "company/center/accelerator/update-exam.html"
    success_message = "عملیات با موفقیت انجام شد"
    slug_field, slug_url_kwarg = "uuid", "uuid"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "ویرایش آزمون"
        context["acc_object"] = self.request.user.access_to_center
        context["question_form"] = QuestionCreateForm
        context["answer_form"] = AnswerCreateForm
        return context

    def get_success_url(self, **kwargs):         
        return reverse_lazy('company:update-exam', args = (self.object.uuid,))
    

class DeleteExam(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Exam
    template_name = "company/center/accelerator/confirm-delete.html"
    success_message = "عملیات با موفقیت انجام شد"
    success_url = reverse_lazy('company:new-exam')
    slug_field, slug_url_kwarg = "uuid", "uuid"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "حذف آزمون"
        return context


@login_required
@require_POST
def new_question(request, exam_uuid):
    exam_instance = Exam.objects.get(uuid=exam_uuid)
    if request.method == 'POST':
        form = request.POST
        form = QuestionCreateForm(form)
        if form.is_valid():
            obj = form.save()
            exam_instance.questions.add(obj)
            exam_instance.save()
            messages.success(request, "عملیات با موفقیت انجام شد")
        else:
            messages.error(request, "مشکلی در فرم وجود دارد!")
    else:
        messages.error(request, "درخاست نامعتبر!")
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


class UpdateQuestion(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Question
    form_class = QuestionCreateForm
    template_name = "company/center/accelerator/update-question.html"
    success_message = "عملیات با موفقیت انجام شد"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "ویرایش سوال"
        context["acc_object"] = self.request.user.access_to_center
        context["answer_form"] = AnswerCreateForm
        return context

    def get_success_url(self, **kwargs):         
        return reverse_lazy('company:update-question', args = (self.object.id,))


@login_required
def delete_question(request, pk):
    try:
        Question.objects.get(pk=pk).delete()
        messages.success(request, "عملیات با موفقیت انجام شد")
    except:
        messages.error(request, "درخاست نامعتبر!")

    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


@login_required
@require_POST
def new_answer(request, question_id):
    question_instance = Question.objects.get(id=question_id)
    if request.method == 'POST':
        form = request.POST
        form = AnswerCreateForm(form)
        if form.is_valid():
            obj = form.save()
            question_instance.answers.add(obj)
            question_instance.save()
            messages.success(request, "عملیات با موفقیت انجام شد")
        else:
            messages.error(request, "مشکلی در فرم وجود دارد!")
    else:
        messages.error(request, "درخاست نامعتبر!")
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


@login_required
def delete_answer(request, pk):
    try:
        Answer.objects.get(pk=pk).delete()
        messages.success(request, "عملیات با موفقیت انجام شد")
    except:
        messages.error(request, "درخاست نامعتبر!")

    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


@login_required
@require_POST
def save_exam_order(request, collection_uuid):
    collection_instance = Collection.objects.get(uuid=collection_uuid)
    if request.method == 'POST':
        form_copy = request.POST.copy()
        form_copy.update({"collection": collection_instance,})

        form = ExamOrderCreateForm(form_copy, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "عملیات با موفقیت انجام شد")
        else:
            messages.error(request, "مشکلی در فرم وجود دارد!")
    else:
        messages.error(request, "درخاست نامعتبر!")
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


@login_required
def delete_exam_order(request, pk):
    try:
        ExamOrder.objects.get(pk=pk).delete()
        messages.success(request, "عملیات با موفقیت انجام شد")
    except:
        messages.error(request, "درخاست نامعتبر!")

    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


@login_required
@require_POST
def new_task(request):
    if request.method == 'POST':
        form = request.POST
        form = TaskCreateForm(form)
        if form.is_valid():
            form.save()
            messages.success(request, "عملیات با موفقیت انجام شد")
        else:
            messages.error(request, "مشکلی در فرم وجود دارد!")
    else:
        messages.error(request, "درخاست نامعتبر!")
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


class UpdateTask(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Task
    form_class = TaskUpdateForm
    template_name = "company/center/accelerator/update-task.html"
    success_message = "عملیات با موفقیت انجام شد"
    slug_field, slug_url_kwarg = "uuid", "uuid"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "ویرایش تسک"
        context["acc_object"] = self.request.user.access_to_center
        return context

    def get_success_url(self, **kwargs):         
        return reverse_lazy('company:update-exam', args = (self.object.uuid,))
    

class DeleteTask(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Task
    template_name = "company/center/accelerator/confirm-delete.html"
    success_message = "عملیات با موفقیت انجام شد"
    success_url = reverse_lazy('company:new-exam')
    slug_field, slug_url_kwarg = "uuid", "uuid"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "حذف آزمون"
        return context


@login_required
@require_POST
def save_task_order(request, collection_uuid):
    collection_instance = Collection.objects.get(uuid=collection_uuid)
    if request.method == 'POST':
        form_copy = request.POST.copy()
        form_copy.update({"collection": collection_instance,})

        form = TaskOrderForm(form_copy, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "عملیات با موفقیت انجام شد")
        else:
            messages.error(request, "مشکلی در فرم وجود دارد!")
    else:
        messages.error(request, "درخاست نامعتبر!")
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


@login_required
def delete_task_order(request, pk):
    try:
        TaskOrder.objects.get(pk=pk).delete()
        messages.success(request, "عملیات با موفقیت انجام شد")
    except:
        messages.error(request, "درخاست نامعتبر!")

    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


class NewSubject(LoginRequiredMixin, View):
    form_class = TopicSubjectCreationForm
    template_name = "company/center/accelerator/new-subject.html"
    context = {"title": "ساخت موضوع جدید"}


    def get(self, request):
        self.context["form"] = self.form_class()
        return render(request, self.template_name, self.context)
    
    def post(self, request):
        if request.method == 'POST':
            form = TopicSubjectCreationForm(request.POST)
            if form.is_valid():
                topic = form.cleaned_data.get('topic', None)
                topic_name = form.cleaned_data.get('topic_name', None)
                subject_name = form.cleaned_data['subject_name']
                if topic_name:
                    topic = Topic.objects.create(name=topic_name, created_by=request.user)
                elif topic:
                    pass
                else:
                    messages.error(request, "امکان ساخت زیرموضوع بدون انتخاب یا ساخت یک موضوع وجود ندارد!")
                    return redirect(reverse('company:new-subject'))
                    
                Subject.objects.create(topic=topic, name=subject_name, created_by=request.user)
                messages.success(request, "عملیات با موفقیت انجام شد")
            else:
                messages.error(request, "مشکلی در فرم وجود دارد!")
        else:
            messages.error(request, "درخاست نامعتبر!")
        return redirect(reverse('company:new-subject'))


class TeamManagement(LoginRequiredMixin, View):
    template_name = "company/center/accelerator/team-management.html"
    context = {"title": "مدیریت تیم ها"}

    def get(self, request):
        acc_object = self.request.user.access_to_center
        self.context["acc_object"] = acc_object
        all_requests = acc_object.accelerator_of_road.first().road_of_road_registration.all()
        
        self.context["approved_requests"] = all_requests.filter(status="a")
        self.context["rejected_requests"] = all_requests.filter(status="r")
        
        filtered_objects = all_requests.exclude(status="n")
        individual_objects = all_requests.exclude(status="n").filter(team_or_individual="i")
        unique_teams = set()
        unique_objects = []

        for obj in filtered_objects:
            if obj.team not in unique_teams:
                unique_teams.add(obj.team)
                if obj.team_or_individual == "t":
                    unique_objects.append(obj)
        combined_results = unique_objects + list(individual_objects)
        self.context["valid_requests"] = combined_results
        self.context["valid_requests_count"] = len(combined_results)
        return render(request, self.template_name, self.context)


class InvestManagement(LoginRequiredMixin, View):
    form_class = TopicSubjectCreationForm
    template_name = "company/center/accelerator/invest-management.html"
    context = {"title": "مدیریت سرمایه گذاری"}

    def get(self, request):
        self.context["acc_object"] = self.request.user.access_to_center
        return render(request, self.template_name, self.context)


class CreatePreRegisterTask(LoginRequiredMixin, View):
    model = PreRegisterTask
    form_class = PreRegisterTaskCreateForm
    template_name = "company/center/accelerator/new-register-task.html"
    success_message = "عملیات با موفقیت انجام شد"
    context = {"title": "مدیریت آزمون های ورودی"}


    def get(self, request):
        self.context["form"] = self.form_class
        self.context["acc_object"] = self.request.user.access_to_center
        return render(request, self.template_name, self.context)
    
    def post(self, request):
        form_copy = request.POST.copy()
        form_copy.update(
            {
                "start_date": date_db_convertor.jdate_edge_convertor(form_copy["start_date"]),
                "expiration_date": date_db_convertor.jdate_edge_convertor(form_copy["expiration_date"]),
            }
        )

        form = self.form_class(form_copy)

        if form.is_valid():
            form.save()
            messages.success(request, self.success_message)
        else:
            messages.error(request, "مشکلی در فرم وجود دارد!")
        
        return redirect(reverse('company:new-register-task'))


class UpdatePreRegisterTask(LoginRequiredMixin, View):
    model = PreRegisterTask
    form_class = PreRegisterTaskUpdateForm
    template_name = "company/center/accelerator/update-register-task.html"
    success_message = "عملیات با موفقیت انجام شد"
    slug_field, slug_url_kwarg = "uuid", "uuid"
    context = {"title": "ویرایش آزمون ورودی"}


    def get(self, request, uuid):
        obj = self.model.objects.get(uuid=uuid)
        self.context["form"] = self.form_class(instance=obj)
        self.context["acc_object"] = self.request.user.access_to_center
        return render(request, self.template_name, self.context)

    def post(self, request, uuid):
        form_copy = request.POST.copy()
        form_copy.update(
            {
                "start_date": date_db_convertor.jdate_edge_convertor(form_copy["start_date"]),
                "expiration_date": date_db_convertor.jdate_edge_convertor(form_copy["expiration_date"]),            }
        )

        obj = self.model.objects.get(uuid=uuid)
        form = self.form_class(form_copy, instance=obj)

        if form.is_valid():
            form.save()
            messages.success(request, self.success_message)
        else:
            messages.error(request, "مشکلی در فرم وجود دارد!")
        
        return redirect(reverse('company:update-register-task', kwargs={'uuid': uuid}))
    

class DeletePreRegisterTask(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = PreRegisterTask
    template_name = "company/center/accelerator/confirm-delete.html"
    success_message = "عملیات با موفقیت انجام شد"
    success_url = reverse_lazy('company:new-register-task')
    slug_field, slug_url_kwarg = "uuid", "uuid"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "حذف آزمون ورودی"
        return context


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def create_center(request):
    if request.method == 'POST':
        try:
            name = request.POST.get("name")
            short_description = request.POST.get("short_description")
            state = request.POST.get("state")
            
            
            # Create a new Center object with the data
            center = Center.objects.create(
                name=name,
                short_description=short_description,
                state=state,
                type="a",
                activity="ثبت نشده",
            )

            # Save the center object
            center.save()

            # Return success response
            return JsonResponse({'message': 'Center created successfully'}, status=201)
        except Exception as e:
            # Return error response if something goes wrong
            return JsonResponse({'error': str(e)}, status=400)
    else:
        # Return method not allowed if request method is not POST
        return JsonResponse({'error': 'Method not allowed'}, status=405)