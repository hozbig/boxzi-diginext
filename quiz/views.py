from django.shortcuts import render, redirect
from django.http import Http404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from django.contrib import messages
from django.urls import reverse
from content.models import Collection, Road
from team.models import RoadRegistration
from django.http import HttpResponseRedirect
from account.models import User
import uuid

from .andaze import send_user_information
from notifier.sms import send_messages
from .models import Exam, UserExamAnsewrHistory, Answer, PreRegisterTask, PreRegisterTaskResponse, PersonalTest, PreRegisterTaskQuestion
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
        task_business_side = road.pre_register_task_for_business_side
        
        registration_obj = user.user_of_road_registration.first()
        
        if registration_obj.team_or_individual == "i":
            self.context["title"] = "به عنوان فرد"
        elif registration_obj.team_or_individual in "ta":
            self.context["title"] = "به عنوان تیم"

        self.context["registration"] = registration_obj
        self.context["task"] = task
        self.context["task_business_side"] = task_business_side
        self.context["road"] = road

        count_of_t_question = task.pre_register_of_pre_register_task_question.count()
        count_of_b_question = task_business_side.pre_register_of_pre_register_task_question.count()
        user_response_count = user.user_of_pre_register_task_response.count()

        if user.user_of_road_registration.first().team_or_individual == "i":
            if user.type == "t":
                if (count_of_t_question - user_response_count) < 1:
                    self.context["challenge_response"] = True
                else:
                    self.context["challenge_response"] = False
            elif user.type == "b":
                if (count_of_b_question - user_response_count) < 1:
                    self.context["challenge_response"] = True
                else:
                    self.context["challenge_response"] = False

                    
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
        road = Road.objects.get(uuid=road_uuid)
        
        # First way (we should use Andaze platform for user characterize analyze behavioral - its toooooo shit)
        if not request.user.user_of_personal_test.exists():
            send_user_information(request.user, road)
        # else:
        #     self.context["object"] = request.user.user_of_personal_test.first()
        
        # ====== Alternative way if the above way is not work properly
        # object = PersonalTest(
        #     user = request.user,
        #     road = road,
        #     reference_id = str(uuid.uuid4()),
        #     first_response_of_sending_information_is_accepted = False,
        # )
        # object.save()
        
        self.context["title"] = "آزمون ورودی شخصیت"
        return render(request, self.template_name, self.context)
    
    
class PersonalTestsResult(LoginRequiredMixin, View):
    template_name = "quiz/personal-tests-result.html"
    context = {}
    
    def get(self, request, user_uuid):
        self.context["title"] = "آزمون ورودی شخصیت"

        try:
            user = User.objects.get(uuid=user_uuid)
        except User.DoesNotExist:
            raise Http404("Given query not found....")

        self.context["object"] = PersonalTest.objects.filter(user=user)
        return render(request, self.template_name, self.context)


class PreRegisterChallenges(LoginRequiredMixin, View):
    template_name = "quiz/pre-register-challenge.html"
    form_class = PreRegisterTaskResponseCreateForm
    context = {}
    
    def get(self, request, task_uuid, road_uuid):
        road = Road.objects.get(uuid=road_uuid)
        self.context["title"] = "تست ورودی"
        self.context["exam_form"] = self.form_class
        self.context["road"] = road
        return render(request, self.template_name, self.context)
    
def save_task_question_response(request, task_uuid, road_uuid):
    task = PreRegisterTask.objects.get(uuid=task_uuid)
    road = Road.objects.get(uuid=road_uuid)

    question = request.POST.get("question")
    question = PreRegisterTaskQuestion.objects.get(id=question)

    try:
        is_answer_exist = PreRegisterTaskResponse.objects.get(user=request.user, question=question)
    except:
        is_answer_exist = False


    form_copy = request.POST.copy()
    form_copy.update(
        {
            "user": request.user,
            "road": road,
            "task": task,
        }
    )

    if is_answer_exist:
        form = PreRegisterTaskResponseCreateForm(form_copy, instance=is_answer_exist)
    else:
        form = PreRegisterTaskResponseCreateForm(form_copy)

    print(form)
    if form.is_valid():
        form.save()
        messages.success(request, "پاسخ شما به چالش با موفقیت ثبت شد")
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
    
    messages.error(request, "مشکلی رخ داده است")
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


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

    def get(self, request, user_uuid):
        self.context["title"] = "مشاهده پاسخ به چالش" 

        try:
            user = User.objects.get(uuid=user_uuid)
        except User.DoesNotExist:
            raise Http404("Given query not found....")

        self.context["object_list"] = PreRegisterTaskResponse.objects.filter(user=user)
        return render(request, self.template_name, self.context)
