from django.shortcuts import render, redirect
from django.db.models import Q
from django.views.generic import View
from django.core.validators import RegexValidator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.urls import reverse
from django.contrib.auth import login, authenticate
from django.utils import timezone
from utils import date_db_convertor
from django.contrib import messages
from content.models import Road
from utils.check_status_user_state_level import add_one_level
from notifier.models import OTP
from notifier.sms import send_messages, send_otp, generate_otp
from notifier.email import send_email
from assessment.models import Question, Response
from plan.models import Plan
from team.models import RoadRegistration, StartUpTeam
from quiz.models import PreRegisterTaskResponse, PersonalTest
from config.settings import DEBUG

from .models import User
from .forms import (
    LoginForm,
    CustomUserChangeForm,
    UserRegisterFormLevel1,
    UserRegisterFormLevel2,
    UserRegisterFormLevel3,
    UserRegisterFormLevel4,
    UserLoginOrRegisterForm,
)
from .mixins import ChangeUserAccessMixin, AnonymousRequiredMixin, RefereeAccessMixin


class LoginOrRegister(AnonymousRequiredMixin, View):
    template_name = "registration/register/login-or-register.html"
    context = {}

    def get(self, request):
        if request.user.is_authenticated and request.user.is_profile_complete_level2():
            return redirect("account:login-or-register")

        self.context["form"] = UserLoginOrRegisterForm
        return render(request, self.template_name, self.context)

    def post(self, request):
        form = UserLoginOrRegisterForm(request.POST)
        phone_number = request.POST.get("phone_number")

        try:
            phone_number = User.objects.get(phone_number=phone_number).phone_number
            messages.info(request, "شماره موبایل شما موجود میباشد، با استفاده از آن وارد شوید")
            return redirect(f"{reverse('account:login')}?phone_number={phone_number}")
        except:
            pass

        if form.is_valid():
            messages.info(request, "شما در سایت عضو نیستید! ثبت نام کنید")
            return redirect(f"{reverse('account:register')}?phone_number={phone_number}")
        
        messages.error(request, "اطلاعات وارد شده صحیح نمیباشد!")
        self.context["form"] = form
        return render(request, self.template_name, self.context)


class UserLoginView(AnonymousRequiredMixin, View):
    template_name = "registration/login.html"

    def get(self, request):
        form = LoginForm()
        return render(request, self.template_name, {'form': form, "DEBUG": DEBUG})

    def post(self, request):        
        form = LoginForm(request.POST)
        
        if form.is_valid():
            phone_number = form.cleaned_data["phone_number"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=phone_number, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "با موفقیت وارد شدید")
                return redirect("router")
            else:
                messages.error(request, "نام کاربری یا رمزعبور واردشده اشتباه می‌باشد!")
        else:
            messages.error(request, "اطلاعات وارد شده صحیح نمیباشد!")
            return render(request, self.template_name, {'form': form})

        return render(request, self.template_name, {'form': form, "DEBUG": DEBUG})


class RegisterLevel1(AnonymousRequiredMixin, View):
    template_name = "registration/register/level1.html"
    context = {}

    def get(self, request):
        is_road = Road.objects.exists()
        if is_road:
            self.context["is_road"] = Road.objects.all().first()
        else:
            self.context["is_road"] = False

        # Check if not phone_number parameter in url redirect use to login-or-register page
        phone_number = request.GET.get('phone_number', None)
        if not phone_number:
            return redirect("account:login-or-register")

        try:
            # Check if the phone_number is not exist in database, if exist the user redirect to login page
            try:
                User.objects.get(phone_number=phone_number)
                return redirect("account:login")
            except:
                pass

            has_any_otp = OTP.objects.filter(phone_number=phone_number).exists()
            if has_any_otp:
                otp_object = OTP.objects.filter(phone_number=phone_number).last()
                if not otp_object.is_valid():
                    generated_otp = generate_otp()
                    OTP.objects.create(otp_code=generated_otp, phone_number=phone_number)
                    send_otp(phone_number, generated_otp)
                    messages.info(request, f"کد یک بارمصرف برای شماره '{phone_number}' پیامک شد")
            else:
                generated_otp = generate_otp()
                OTP.objects.create(otp_code=generated_otp, phone_number=phone_number)
                send_otp(phone_number, generated_otp)
                messages.info(request, f"کد یک بارمصرف برای شماره '{phone_number}' پیامک شد")
        except:
            pass

        self.context["form"] = UserRegisterFormLevel1
        return render(request, self.template_name, self.context)

    def post(self, request):
        try:
            road = Road.objects.first()
        except:
            messages.error(request, "مسیری برای ثبت نام پیدا نشد")
            return render(request, self.template_name, self.context) 

        team_or_individual = request.POST.get("team_or_individual")
        if not team_or_individual in "ti":
            messages.error(request, "شما باید یکی از روش های تیم یا فرد را انتخاب کنید!")
            self.context["form"] = request.POST
            return render(request, self.template_name, self.context) 

        form = UserRegisterFormLevel1(request.POST)
        if form.is_valid():
            user_otp_code = request.POST.get("otp_code", None)
            if not user_otp_code:
                messages.error(request, "کد یکبار مصرف وارد شده، صحیح نمیباشد!")
                return self.get(request)

            phone_number = request.POST.get("phone_number")
            otp_code = OTP.objects.filter(phone_number=phone_number).last()
            if not otp_code.is_valid():
                messages.error(request, "کد وارد شده منقضی شده است!")
                return self.get(request)
            
            if not user_otp_code == otp_code.otp_code:
                messages.error(request, "کد وارد شده اشتباه می‌باشد! دوباره تلاش کنید")
                return self.get(request)

            user = form.save(commit=False)
            user.is_team_member = True
            user.save()

            try:
                registration_obj = RoadRegistration.objects.get(user=request.user)
                return redirect("router")
            except:
                registration_obj = RoadRegistration(
                    user=user,
                    road=road,
                    status="n",
                    status_user_state="2",
                    team_or_individual=team_or_individual,
                )
                registration_obj.save()

            login(request, user)
            
            send_messages(
                action="initial_registration_success",
                destination_phone_number=user.phone_number,
                user=request.user.first_name,
            )
            
            messages.success(request, "اکنون اطلاعات خودرا تکمیل کنید")
            return redirect("account:register2")

        messages.error(request, "اطلاعات وارد شده صحیح نمیباشد!")
        self.context["form"] = form
        is_road = Road.objects.exists()
        if is_road:
            self.context["is_road"] = Road.objects.all().first()
        else:
            self.context["is_road"] = False
        return render(request, self.template_name, self.context)


class RegisterLevel2(LoginRequiredMixin, View):
    template_name = "registration/register/level2.html"
    context = {}

    def get(self, request):
        registration_obj = RoadRegistration.objects.filter(user=request.user).first()
            
        if int(registration_obj.status_user_state) != 2:
            return redirect("router")
        
        self.context["form"] = UserRegisterFormLevel2(instance=request.user)
        return render(request, self.template_name, self.context)

    def post(self, request):
        registration_obj = RoadRegistration.objects.filter(user=request.user).first()
        if int(registration_obj.status_user_state) != 2:
            return redirect("router")

        form_copy = request.POST.copy()
        form_copy.update({
            "birthday": date_db_convertor.jdate_edge_convertor(form_copy["birthday"])
        })

        form = UserRegisterFormLevel2(form_copy, instance=request.user)
        if form.is_valid():
            form.save()
            registration_obj.status_user_state = add_one_level(registration_obj.status_user_state)
            registration_obj.save()

            messages.success(request, "ثبت شد، ادامه دهید.")
            return redirect("account:register3")
        
        messages.error(request, "اطلاعات وارد شده صحیح نمی‌باشد!")
        self.context["form"] = form 
        return render(request, self.template_name, self.context)
    

class RegisterLevel3(LoginRequiredMixin, View):
    template_name = "registration/register/level3.html"
    context = {}

    def get(self, request):
        registration_obj = RoadRegistration.objects.filter(user=request.user).first()
        if int(registration_obj.status_user_state) != 3:
            return redirect("router")

        self.context["form"] = UserRegisterFormLevel3(instance=request.user)
        return render(request, self.template_name, self.context)

    def post(self, request):
        registration_obj = RoadRegistration.objects.filter(user=request.user).first()
        if int(registration_obj.status_user_state) != 3:
            return redirect("router")
        
        form = UserRegisterFormLevel3(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            registration_obj.status_user_state = add_one_level(registration_obj.status_user_state)
            registration_obj.save()

            messages.success(request, "به مرحله آخر خوش آمدید.")
            return redirect("account:register4")
        
        messages.error(request, "اطلاعات وارد شده صحیح نمی‌باشد!")
        self.context["form"] = form 
        return render(request, self.template_name, self.context)


class RegisterLevel4(LoginRequiredMixin, View):
    template_name = "registration/register/level4.html"
    context = {}

    def get(self, request):
        registration_obj = RoadRegistration.objects.filter(user=request.user).first()
        if int(registration_obj.status_user_state) != 4:
            return redirect("router")
        
        self.context["form"] = UserRegisterFormLevel4(instance=request.user)
        return render(request, self.template_name, self.context)

    def post(self, request):
        registration_obj = RoadRegistration.objects.filter(user=request.user).first()
        if int(registration_obj.status_user_state) != 4:
            return redirect("router")
    
        form = UserRegisterFormLevel4(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            registration_obj.status_user_state = add_one_level(registration_obj.status_user_state)
            registration_obj.complete_registration_date = timezone.datetime.now()
            registration_obj.save()
            
            send_messages(
                action="final_registration_success",
                destination_phone_number=request.user.phone_number,
                user=request.user.first_name,
            )
            send_email(template="welcome", user=request.user)
            messages.success(request, "ثبت نام شما در باکس زی کامل شد. جهت ثبت درخواست برای مسیر آموزشی مورد نظر فرایند هارو از طریق راهنمای داخل داشبورد خود ادامه بدید.")
            return redirect("account:user-dashboard")
        
        messages.error(request, "اطلاعات وارد شده صحیح نمی‌باشد!")
        self.context["form"] = form 
        return render(request, self.template_name, self.context)


class UserProfile(LoginRequiredMixin, View):
    template_name = "account/user-profile.html"
    success_message = "پروفایل شما با موفقیت ویرایش شد."
    context = {"title": "پروفایل کاربر"}

    def get(self, request, uuid):
        user = User.objects.get(uuid=uuid)
        self.context["object"] = user
        self.context["next_url"] = request.GET.get('next', None)
        return render(request, self.template_name, self.context)
    

class ChangeUser(LoginRequiredMixin, ChangeUserAccessMixin, View):
    form_class = CustomUserChangeForm
    template_name = "account/change-user.html"
    success_message = "پروفایل شما با موفقیت ویرایش شد."
    context = {"title": "ویرایش کاربر"}

    def get(self, request, uuid):
        user = User.objects.get(uuid=uuid)
        self.context["object"] = user
        self.context["form"] = self.form_class(instance=user)
        # self.context["experience_form"] = WorkExperienceCreateForm

        return render(request, self.template_name, self.context)

    def post(self, request, uuid):
        user = User.objects.get(uuid=uuid)

        form = self.form_class(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, self.success_message)
            next_url = request.POST.get('next')
            return redirect(next_url if next_url else reverse("router"))
        else:
            messages.error(request, "مشکلی در فرم وجود دارد!")
            
        self.context["object"] = user
        self.context["form"] = form
        return render(request, self.template_name, self.context)


class UserDashboard(LoginRequiredMixin, View):
    template_name = "account/dashboard.html"
    context = {"title":"داشبورد کاربر"}

    def get(self, request):
        self.context["registration_obj"] = RoadRegistration.objects.get(user=request.user)
        return render(request, self.template_name, self.context)


class RefereeDashboard(LoginRequiredMixin, RefereeAccessMixin, View):
    template_name = "account/referee/dashboard.html"
    context = {"title":"داشبورد داور"}

    def get(self, request):
        acc_object = self.request.user.referee_of_center.first()
        all_requests = acc_object.accelerator_of_road.first().road_of_road_registration.all().filter(
            (Q(team_or_individual="t") | Q(team_or_individual="i")) & Q(complete_registration_date__isnull=False))
        
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
        
        self.context["valid_requests_count"] = len(combined_results)
        self.context["valid_requests"] = combined_results
        return render(request, self.template_name, self.context)


class JudgmentPage(LoginRequiredMixin, RefereeAccessMixin, View):
    template_name = "account/referee/judgment_page.html"
    context = {}

    def get(self, request, user_uuid):
        user = User.objects.get(uuid=user_uuid)
        if user.user_of_team_member.exists():
            team = user.user_of_team_member.first().team
            plan = team.team_of_plan.first()
            self.context["user_object"] = user
            self.context["object"] = f"تیم {team}"
            self.context["team"] = team
            self.context["plan"] = plan
            self.context["title"] = "داوری تیم"
        else:
            plan = user.user_of_plan.first()
            self.context["user_object"] = user
            self.context["object"] = user.last_name
            self.context["team"] = None
            self.context["plan"] = plan
            self.context["title"] = "داوری فرد"
        
        self.context["plan_questions"] = Question.objects.filter(category__key_name="plan")
        self.context["individual_questions"] = Question.objects.filter(category__key_name="individual")
        self.context["team_questions"] = Question.objects.filter(category__key_name="team")
        self.context["challenge_questions"] = Question.objects.filter(
            Q(category__key_name="challenge_tech") | Q(category__key_name="challenge_business")
        )
        return render(request, self.template_name, self.context)
    
    def post(self, request, user_uuid):
        form_copy = request.POST.copy()
        
        # Get needed related uuid
        plan_uuid = form_copy.get("plan")
        team_uuid = form_copy.get("team")
        individual_uuid = form_copy.get("individual")
        pre_register_challenge_uuid = form_copy.get("pre_register_change")
        # Delete data
        form_copy.pop("plan", None)
        form_copy.pop("team", None)
        form_copy.pop("individual", None)
        form_copy.pop("pre_register_change", None)
        form_copy.pop("csrfmiddlewaretoken", None)
        # Get objects from models
        plan = Plan.objects.filter(uuid=plan_uuid).first()
        team = StartUpTeam.objects.filter(uuid=team_uuid).first()
        individual = User.objects.filter(uuid=individual_uuid).first()
        pre_register_challenge = PreRegisterTaskResponse.objects.filter(uuid=pre_register_challenge_uuid).first()
        
        for item in form_copy:
            question = Question.objects.get(uuid=item)
            point = int(form_copy[item].split('.')[0])
            try:
                with transaction.atomic():
                    response = Response.objects.create(
                        referee=request.user,
                        question=question,
                        point=point,
                        plan=plan,
                        team=team,
                        individual=individual,
                        pre_register_change=pre_register_challenge,
                    )
            except Exception as e:

        messages.success(request, "عملیات با موفقیت انجام شد")
        return redirect(reverse('account:judgment-page', kwargs={'user_uuid': user_uuid}))
        return render(request, self.template_name, self.context)
