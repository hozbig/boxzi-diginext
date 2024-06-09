from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from django.contrib import messages
from django.urls import reverse
from content.models import Collection, Road
from team.models import RoadRegistration
from django.http import HttpResponseRedirect
from account.models import User
from utils.check_status_user_state_level import add_one_level

from .models import Exam, UserExamAnsewrHistory, Answer, PreRegisterTask, PreRegisterTaskResponse, PersonalTest
from .forms import PreRegisterTaskResponseCreateForm, PreRegisterTaskResponseUpdateForm


class ExamDetail(LoginRequiredMixin, View):
    model = Exam
    template_name = "quiz/exam-detail.html"
    context = {}
    
    def get(self, request, exam_uuid, collection_uuid):
        object = self.model.objects.get(uuid=exam_uuid)
        collection = Collection.objects.get(uuid=collection_uuid)
        exam_history = UserExamAnsewrHistory.objects.filter(user=request.user, exam=object)

        self.context["title"] = f"آزمون {object.name}"
        self.context["object"] = object
        self.context["collection"] = collection
        self.context["exam_history"] = exam_history
        self.context["count_of_valid_answer"] = exam_history.filter(answer__is_valid=True).count()
        return render(self.request, self.template_name, self.context)
    
    def post(self, request, exam_uuid, collection_uuid):
        user = request.user
        exam = Exam.objects.get(uuid=exam_uuid)
        questions = exam.questions.all()
        answers_list = []

        for question in questions:
            answer_id = request.POST.get(f'answer-name-{exam.uuid}{question.id}')
            try:
                answer = Answer.objects.get(id=answer_id)
            except:
                messages.error(request, "خطا! مطمئن شوید تمام سوال ها پاسخ داده شده اند. et1")
                return redirect(reverse('quiz:exam-detail', args=[exam_uuid]))
            answers_list.append([user, exam, question, answer])

        if len(answers_list) == len(questions):
            for i in answers_list:
                UserExamAnsewrHistory.objects.create(
                    user=i[0],
                    exam=i[1],
                    question=i[2],
                    answer=i[3]
                )
            if exam.medals:
                user.received_medals = (user.received_medals or 0) + exam.medals
                user.save()
        else:
            messages.error(request, "خطا! مطمئن شوید تمام سوال ها پاسخ داده شده اند. et2")
            return redirect(reverse('quiz:exam-detail', args=[exam_uuid, collection_uuid]))

        messages.success(request, "آزمون شما با موفقیت ثبت شد")
        return redirect(reverse('quiz:exam-detail', args=[exam_uuid, collection_uuid]))

# ------- OLD PreRegisterRequired -------
# class PreRegisterRequired(LoginRequiredMixin, View):
#     template_name = "quiz/pre-register-required.html"
#     context = {}
    
#     def get(self, request, road_uuid):
#         user = request.user
#         road = Road.objects.get(uuid=road_uuid)
#         registration_obj = user.user_of_road_registration.first()

#         if not registration_obj.status_user_state == "1":
#             if registration_obj.status_user_state == "2t":
#                 return redirect(reverse('quiz:pre-register-required-team', args=[road_uuid]))
#             elif registration_obj.status_user_state == "2i":
#                 return redirect(reverse('quiz:pre-register-required-individual', args=[road_uuid]))

#         self.context["title"] = "تیم یا فرد؟"
#         self.context["road"] = road
#         return render(request, self.template_name, self.context)

class PreRegisterRequired(LoginRequiredMixin, View):
    template_name = "quiz/pre-register-required-team.html"
    context = {}
    
    def get(self, request, road_uuid):
        user = request.user
        road = Road.objects.get(uuid=road_uuid)
        task = road.pre_register_task
        
        registration_obj = user.user_of_road_registration.first()
        
        self.context["title"] = "به عنوان تیم"
        self.context["registration"] = registration_obj
        self.context["task"] = task
        self.context["road"] = road
        if user.user_of_road_registration.first().team_or_individual == "i":
            self.context["challenge_response"] = user.user_of_pre_register_task_response.exists()
        return render(request, self.template_name, self.context)
    
    def post(self, request, task_uuid, road_uuid):
        task = PreRegisterTask.objects.get(uuid=task_uuid)
        road = Road.objects.get(uuid=road_uuid)
        
        messages.success(request, "درخواست شما با موفقیت ثبت شد")
        return redirect(reverse('quiz:pre-register-required-team', args=[task_uuid, road_uuid]))

class PreRegisterRequiredTeam(LoginRequiredMixin, View):
    template_name = "quiz/pre-register-required-team.html"
    context = {}
    
    def get(self, request, road_uuid):
        user = request.user
        road = Road.objects.get(uuid=road_uuid)
        task = road.pre_register_task
        
        registration_obj = user.user_of_road_registration.first()
        registration_obj.status_user_state = "2t"
        registration_obj.save()
        
        self.context["title"] = "به عنوان تیم"
        self.context["registration"] = registration_obj
        self.context["task"] = task
        self.context["road"] = road
        return render(request, self.template_name, self.context)
    
    def post(self, request, task_uuid, road_uuid):
        task = PreRegisterTask.objects.get(uuid=task_uuid)
        road = Road.objects.get(uuid=road_uuid)
        
        messages.success(request, "درخواست شما با موفقیت ثبت شد")
        return redirect(reverse('quiz:pre-register-required-team', args=[task_uuid, road_uuid]))
    
    
class PreRegisterRequiredIndividual(LoginRequiredMixin, View):
    template_name = "quiz/pre-register-required-individual.html"
    context = {}
    
    def get(self, request, task_uuid, road_uuid):
        task = PreRegisterTask.objects.get(uuid=task_uuid)
        road = Road.objects.get(uuid=road_uuid)

        try:
            registration_obj = RoadRegistration.objects.get(road=road, user=request.user)        
            if registration_obj.status_user_state in "fm":
                return redirect(reverse('team:road-registration', args=[road_uuid]))
        except:
            registration_obj = False
        
        if not registration_obj:
            registration_obj = RoadRegistration(
                user=request.user,
                road=road,
                status="w",
                status_user_state="i",
            )
            registration_obj.save()
            return redirect(reverse('quiz:pre-register-required-individual', args=[task_uuid, road_uuid]))
        else:
            self.context["registration"] = registration_obj

        try:
            self.context["challenge_response"] = PreRegisterTaskResponse.objects.get(user=request.user, task=task, road=road)
        except:
            self.context["challenge_response"] = False
            return redirect(reverse('quiz:pre-register-required', args=[task_uuid, road_uuid]))

        
        self.context["title"] = "نیازمندی های این مسیر"
        self.context["task"] = task
        self.context["road"] = road
        return render(request, self.template_name, self.context)
    
    def post(self, request, task_uuid, road_uuid):
        task = PreRegisterTask.objects.get(uuid=task_uuid)
        road = Road.objects.get(uuid=road_uuid)
        
        messages.success(request, "درخواست شما با موفقیت ثبت شد")
        return redirect(reverse('quiz:pre-register-required-individual', args=[task_uuid, road_uuid]))


@login_required
def i_am_team_individual(request, uuid):
    try:
        obj = RoadRegistration.objects.get(uuid=uuid)
        obj.status_user_state = "f"
        obj.save()
        messages.success(request, "درخواست شما ثبت شد")
        messages.info(request, "درخواست شما برای شرکت در این برنامه به صورت فردی ثبت شد، منتظر تایید از طرف شتابدهنده بمانید.")
        return redirect(reverse('team:road-registration', kwargs={'uuid': obj.road.uuid}))
    except:
        messages.error(request, "درخاست نامعتبر!")

    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
    

@login_required
def i_am_team_member(request, uuid):
    if request.method == 'POST':
        team_name = request.POST.get("team_name")
        obj = RoadRegistration.objects.get(uuid=uuid)
        obj.status_user_state = "m"
        obj.team_name = team_name
        obj.save()
        messages.success(request, "درخواست شما ثبت شد")
        messages.info(request, "درخواست شما برای شرکت در این مسیرآموزشی ثبت شد، برای ثبت نهایی درخواست هماهنگ کننده تیم هم باید درخواست، تیمی را انجام داده باشد.")
        return redirect(reverse('team:road-registration', kwargs={'uuid': obj.road.uuid}))
    else:
        messages.error(request, "درخاست نامعتبر!")
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


@login_required
def i_am_team_coordinator(request, uuid):
    try:
        obj = RoadRegistration.objects.get(uuid=uuid)
        obj.status_user_state = "c"
        obj.save()
    except:
        messages.error(request, "درخاست نامعتبر!")

    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


class PreRegisterPersonalTests(LoginRequiredMixin, View):
    template_name = "quiz/pre-register-personal-tests.html"
    context = {}
    
    def get(self, request, road_uuid):
        if request.user.user_of_personal_test.first():
                return redirect("router")
        self.context["title"] = "آزمون ورودی شخصیت"
        return render(request, self.template_name, self.context)
    
    def post(self, request, road_uuid):
        if request.user.user_of_personal_test.first():
                return redirect("router")

        road = Road.objects.get(uuid=road_uuid)
        PersonalTest.objects.create(user=request.user, road=road)

        next_url = request.GET.get('next')
        messages.success(request, "آزمون شما با موفقیت ثبت شد")
        return redirect(next_url if next_url else reverse("quiz:pre-register-required", kwargs={"road_uuid": road_uuid,}))


class PreRegisterChallenges(LoginRequiredMixin, View):
    template_name = "quiz/pre-register-challenge.html"
    form_class = PreRegisterTaskResponseCreateForm
    context = {}
    
    def get(self, request, task_uuid, road_uuid):
        if request.user.user_of_pre_register_task_response.exists():
            messages.error(request, "عملیات غیرمجاز !")
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

        task = PreRegisterTask.objects.get(uuid=task_uuid)
        road = Road.objects.get(uuid=road_uuid)
        self.context["title"] = "تست ورودی"
        self.context["exam_form"] = self.form_class
        self.context["task"] = task
        self.context["road"] = road
        return render(request, self.template_name, self.context)
    
    def post(self, request, task_uuid, road_uuid):
        if request.user.user_of_pre_register_task_response.exists():
            messages.error(request, "عملیات غیرمجاز !")
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

        task = PreRegisterTask.objects.get(uuid=task_uuid)
        road = Road.objects.get(uuid=road_uuid)

        form_copy = request.POST.copy()
        form_copy.update(
            {
                "user": request.user,
                "road": road,
                "task": task,
            }
        )

        form = self.form_class(form_copy, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "پاسخ شما به چالش با موفقیت ثبت شد")
            next_url = request.GET.get('next')
            return redirect(next_url if next_url else reverse("quiz:pre-register-required", kwargs={"task_uuid": task_uuid, "road_uuid": road_uuid,}))
        
        messages.error(request, "مشکلی پیش آمده است!")
        self.context["title"] = "تست ورودی"
        self.context["exam_form"] = form
        self.context["task"] = task
        self.context["road"] = road
        return render(request, self.template_name, self.context)


class PreRegisterChallengesUpdate(LoginRequiredMixin, View):
    template_name = "quiz/pre-register-challenge-update.html"
    form_class = PreRegisterTaskResponseUpdateForm
    context = {}
    
    def get(self, request, task_res_uuid, road_uuid):
        task = PreRegisterTaskResponse.objects.get(uuid=task_res_uuid)
        road = Road.objects.get(uuid=road_uuid)
        self.context["title"] = "ویرایش پاسخ چالش ورودی"
        self.context["exam_form"] = self.form_class(instance=task)
        self.context["task"] = task
        self.context["road"] = road
        return render(request, self.template_name, self.context)
    
    def post(self, request, task_res_uuid, road_uuid):
        task = PreRegisterTaskResponse.objects.get(uuid=task_res_uuid)
        road = Road.objects.get(uuid=road_uuid)

        form = self.form_class(request.POST, request.FILES, instance=task)
        print(form)
        if form.is_valid():
            form.save()
            messages.success(request, "پاسخ شما به چالش با موفقیت ویرایش شد")
            next_url = request.GET.get('next')
            return redirect(next_url if next_url else reverse("quiz:pre-register-required", kwargs={"task_uuid": task.task.uuid, "road_uuid": road_uuid,}))
        
        messages.error(request, "مشکلی پیش آمده است!")
        self.context["title"] = "ویرایش پاسخ چالش ورودی"
        self.context["exam_form"] = self.form_class(instance=task)
        self.context["task"] = task
        self.context["road"] = road
        return render(request, self.template_name, self.context)


class PreRegisterTaskResponseDetail(LoginRequiredMixin, View):
    model = PreRegisterTaskResponse
    template_name = "quiz/task-response-detail.html"
    context = {}

    def get(self, request, road_uuid, username):
        road = Road.objects.get(uuid=road_uuid)
        user = User.objects.get(username=username)
        self.context["title"] = "مشاهده پاسخ به چالش" 
        self.context["object"] = PreRegisterTaskResponse.objects.get(user=user, road=road)
        return render(request, self.template_name, self.context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
