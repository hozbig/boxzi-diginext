from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, ListView, View, CreateView, UpdateView, DeleteView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib.auth.hashers import make_password
from django.utils.crypto import get_random_string
from notifier.sms import send_messages
from notifier.email import send_email
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
from quiz.models import Exam, Question, Answer, ExamOrder, Task, TaskOrder, PreRegisterTask, PreRegisterTaskQuestion, PersonalTest
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
    PreRegisterTaskQuestionCreateForm
)
from subject.models import Topic, Subject
from subject.forms import TopicSubjectCreationForm
from account.models import User
from account.forms import AddRefereeForm
from team.models import RoadRegistration

from .models import Company, Center
from .mixins import CompanyAdminMixin, AcceleratorAdminMixin


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


class AcceleratorDashboard(LoginRequiredMixin, AcceleratorAdminMixin, View):
    model = Center
    template_name = "company/center/dashboard.html"
    context = {
        "title": "داشبورد شتابدهنده",
    }

    def get(self, request):
        user = request.user
        object = user.access_to_center
        self.context["object"] = object
        self.context["roads_count"] = object.accelerator_of_road.count()
        self.context["active_roads_count"] = object.accelerator_of_road.count()
        try:
            all_requests = object.accelerator_of_road.first().road_of_road_registration.all()
            approved_requests_count = all_requests.filter(status="a").count()
            
            self.context["requests_count"] = all_requests.count()
            self.context["approve_percentage"] = round(100 * float(approved_requests_count)/float(all_requests.count()))
            
            self.context["personal_requests_count"] = all_requests.filter(team_or_individual="i").count()
            self.context["team_requests_count"] = all_requests.filter(team_or_individual__in=["t", "a"]).count()
            self.context["complete_requests"] = all_requests.filter(status_user_state="5").count()
            self.context["incomplete_requests"] = all_requests.exclude(status_user_state="5").count()
            
            self.context["all_challenge"] = PreRegisterTask.objects.count()
            self.context["all_personal_test"] = PersonalTest.objects.count()
        except:
            pass

        return render(request, self.template_name, self.context)


class CreateRoad(LoginRequiredMixin, AcceleratorAdminMixin, View):
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

    
class UpdateRoad(LoginRequiredMixin, AcceleratorAdminMixin, View):
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
            return redirect(reverse('company:update-road', kwargs={'uuid': uuid}))
        
        messages.error(request, "مشکلی در فرم وجود دارد!")
        return redirect(reverse('company:update-road', kwargs={'uuid': uuid}))
    

class DeleteRoad(LoginRequiredMixin, AcceleratorAdminMixin, SuccessMessageMixin, DeleteView):
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
    

class CreateCollection(LoginRequiredMixin, AcceleratorAdminMixin, SuccessMessageMixin, CreateView):
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


class UpdateCollection(LoginRequiredMixin, AcceleratorAdminMixin, SuccessMessageMixin, UpdateView):
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
    

class DeleteCollection(LoginRequiredMixin, AcceleratorAdminMixin, SuccessMessageMixin, DeleteView):
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


class CreateContent(LoginRequiredMixin, AcceleratorAdminMixin, SuccessMessageMixin, CreateView):
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


class UpdateContent(LoginRequiredMixin, AcceleratorAdminMixin, SuccessMessageMixin, UpdateView):
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
    

class DeleteContent(LoginRequiredMixin, AcceleratorAdminMixin, SuccessMessageMixin, DeleteView):
    model = Content
    template_name = "company/center/accelerator/confirm-delete.html"
    success_message = "عملیات با موفقیت انجام شد"
    success_url = reverse_lazy('company:new-content')
    slug_field, slug_url_kwarg = "uuid", "uuid"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "حذف گام"
        return context
    

class CreateExam(LoginRequiredMixin, AcceleratorAdminMixin, SuccessMessageMixin, CreateView):
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


class UpdateExam(LoginRequiredMixin, AcceleratorAdminMixin, SuccessMessageMixin, UpdateView):
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
    

class DeleteExam(LoginRequiredMixin, AcceleratorAdminMixin, SuccessMessageMixin, DeleteView):
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


class UpdateQuestion(LoginRequiredMixin, AcceleratorAdminMixin, SuccessMessageMixin, UpdateView):
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


class UpdateTask(LoginRequiredMixin, AcceleratorAdminMixin, SuccessMessageMixin, UpdateView):
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
        return reverse_lazy('company:update-task', args = (self.object.uuid,))
    

class DeleteTask(LoginRequiredMixin, AcceleratorAdminMixin, SuccessMessageMixin, DeleteView):
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


class TeamManagement(LoginRequiredMixin, AcceleratorAdminMixin, View):
    template_name = "company/center/accelerator/team-management.html"
    context = {"title": "مدیریت تیم ها"}

    def get(self, request):
        acc_object = self.request.user.access_to_center
        self.context["acc_object"] = acc_object
        # all_requests = acc_object.accelerator_of_road.first().road_of_road_registration.all().filter(
        #     (Q(team_or_individual="t") | Q(team_or_individual="i")) & Q(complete_registration_date__isnull=False))

        all_requests = acc_object.accelerator_of_road.first().road_of_road_registration.all()
        
        self.context["all_requests"] = all_requests
        self.context["last_10_requests"] = all_requests.order_by("-id")[:10]
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
    

class AllRequests(LoginRequiredMixin, AcceleratorAdminMixin, View):
    template_name = "company/center/accelerator/all-requests.html"
    context = {"title": "لیست کامل درخواست ها"}

    def get(self, request):
        acc_object = self.request.user.access_to_center
        self.context["acc_object"] = acc_object
        # object_list = acc_object.accelerator_of_road.first().road_of_road_registration.all().filter(
        #     (Q(team_or_individual="t") | Q(team_or_individual="i")) & Q(complete_registration_date__isnull=False))
        
        object_list = acc_object.accelerator_of_road.first().road_of_road_registration.all()
        
        self.context["object_list"] = object_list.order_by("-id")
        self.context["approved_requests"] = object_list.filter(status="a")
        self.context["rejected_requests"] = object_list.filter(status="r")

        filtered_objects = object_list.exclude(status="n")
        individual_objects = object_list.exclude(status="n").filter(team_or_individual="i")
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


class InvestManagement(LoginRequiredMixin, AcceleratorAdminMixin, View):
    form_class = TopicSubjectCreationForm
    template_name = "company/center/accelerator/invest-management.html"
    context = {"title": "مدیریت سرمایه گذاری"}

    def get(self, request):
        self.context["acc_object"] = self.request.user.access_to_center
        return render(request, self.template_name, self.context)


class CreatePreRegisterTask(LoginRequiredMixin, AcceleratorAdminMixin, View):
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

        form = self.form_class(form_copy)

        if form.is_valid():
            form.save()
            messages.success(request, self.success_message)
        else:
            messages.error(request, "مشکلی در فرم وجود دارد!")
        
        return redirect(reverse('company:new-register-task'))


class UpdatePreRegisterTask(LoginRequiredMixin, AcceleratorAdminMixin, View):
    model = PreRegisterTask
    form_class = PreRegisterTaskUpdateForm
    template_name = "company/center/accelerator/update-register-task.html"
    success_message = "عملیات با موفقیت انجام شد"
    slug_field, slug_url_kwarg = "uuid", "uuid"
    context = {"title": "ویرایش آزمون ورودی"}

    def get(self, request, uuid):
        obj = self.model.objects.get(uuid=uuid)
        self.context["form"] = self.form_class(instance=obj)
        self.context["question_form"] = PreRegisterTaskQuestionCreateForm
        self.context["object"] = obj
        self.context["acc_object"] = self.request.user.access_to_center
        return render(request, self.template_name, self.context)

    def post(self, request, uuid):
        form_copy = request.POST.copy()

        obj = self.model.objects.get(uuid=uuid)
        form = self.form_class(form_copy, instance=obj)

        if form.is_valid():
            form.save()
            messages.success(request, self.success_message)
        else:
            messages.error(request, "مشکلی در فرم وجود دارد!")
        
        return redirect(reverse('company:update-register-task', kwargs={'uuid': uuid}))
    

@login_required
@require_POST
def save_pre_register_task_question(request, pre_register_task_uuid):
    pre_register_task_object = PreRegisterTask.objects.get(uuid=pre_register_task_uuid)
    if request.method == 'POST':
        form_copy = request.POST.copy()
        form_copy.update({"pre_register": pre_register_task_object,"accelerator": pre_register_task_object.accelerator})

        form = PreRegisterTaskQuestionCreateForm(form_copy)
        if form.is_valid():
            form.save()
            messages.success(request, "عملیات با موفقیت انجام شد")
        else:
            messages.error(request, "مشکلی در فرم وجود دارد!")
    else:
        messages.error(request, "درخاست نامعتبر!")
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


@login_required
def delete_pre_register_task_question(request, uuid):
    try:
        PreRegisterTaskQuestion.objects.get(uuid=uuid).delete()
        messages.success(request, "عملیات با موفقیت انجام شد")
    except:
        messages.error(request, "درخاست نامعتبر!")

    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


class DeletePreRegisterTask(LoginRequiredMixin, AcceleratorAdminMixin, SuccessMessageMixin, DeleteView):
    model = PreRegisterTask
    template_name = "company/center/accelerator/confirm-delete.html"
    success_message = "عملیات با موفقیت انجام شد"
    success_url = reverse_lazy('company:new-register-task')
    slug_field, slug_url_kwarg = "uuid", "uuid"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "حذف آزمون ورودی"
        return context
    
    
class RefereeManagement(LoginRequiredMixin, AcceleratorAdminMixin, View):
    model = User
    form_class = AddRefereeForm
    template_name = "company/center/accelerator/referee-management.html"
    context = {}
    
    def get(self, request):
        self.context["title"] = "مدیریت داورها"
        self.context["form"] = self.form_class
        return render(request, self.template_name, self.context)
    
    def post(self, request):
        if not request.user.is_center_staff:
            messages.error(request, "عملیات غیرمجاز! شما ادمین شتابدهنده نیستید.")
            return render(request, self.template_name, self.context)
        
        form_copy = request.POST.copy()
        form_copy.update({"referee_validity_date": date_db_convertor.jdate_edge_convertor(form_copy["referee_validity_date"]),})
        
        form = self.form_class(form_copy)
        if form.is_valid():
            phone_number = form.cleaned_data["phone_number"]
            email = form.cleaned_data["email"]
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            referee_validity_date = form.cleaned_data["referee_validity_date"]
            referee_type = form.cleaned_data["referee_type"]
            user_objects = User.objects.filter(phone_number=phone_number)
            
            if not user_objects.exists():
                # Generated_pass is the password can login with it
                generated_pass = get_random_string(length=10)
                hashed_password = make_password(generated_pass)
                user_obj = User.objects.create(
                    phone_number = phone_number,
                    email = email,
                    first_name = first_name,
                    last_name = last_name,
                    referee_validity_date = referee_validity_date,
                    password = hashed_password,
                    referee_type= referee_type,
                    is_referee = True
                )
                # Add user(referee) to center(accelerator) valid referees
                center_obj = request.user.access_to_center
                center_obj.referees.add(user_obj)
                center_obj.save()
                
                send_messages(
                    action="invitation_to_jury",
                    destination_phone_number=user_obj.phone_number,
                    user=user_obj.first_name,
                )
                send_messages(
                    action="username_password",
                    destination_phone_number=user_obj.phone_number,
                    user=user_obj.first_name,
                    password=generated_pass,
                )
                send_email(template="authentication_info", user=user_obj, password=generated_pass)
                
                messages.success(request, "عملیات با موفقیت انجام شد")
                return redirect("company:referee-management")
            else:
                messages.error(request, "این کاربر از قبل ثبت نام کرده است!")
                return redirect("company:referee-management")
        else:
            self.context["form"] = self.form_class
            messages.error(request, "مشکلی در فرم وجود دارد!")
            return render(request, self.template_name, self.context)


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