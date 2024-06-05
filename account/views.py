from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.contrib.auth import login, authenticate
from django.utils import timezone
from content.models import WatchedContent
from utils import date_db_convertor
from django.contrib import messages
from content.models import Road
from team.models import RoadRegistration
from utils.check_status_user_state_level import add_one_level, level_checker


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
from .mixins import ChangeUserAccessMixin, AnonymousRequiredMixin


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
        return render(request, self.template_name, {'form': form})

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
                messages.error(request, "aaaa!")
        else:
            messages.error(request, "اطلاعات وارد شده صحیح نمیباشد!")

        return render(request, self.template_name, {'form': form})


class RegisterLevel1(AnonymousRequiredMixin, View):
    template_name = "registration/register/level1.html"
    context = {}

    def get(self, request):
        try:
            self.context["is_road"] = Road.objects.first()
        except:
            self.context["is_road"] = False

            try:
                re_obj = RoadRegistration.objects.get(user=request.user)
                return redirect("router")
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
            user = form.save(commit=False)
            user.is_team_member = True
            user.save()

            try:
                re_obj = RoadRegistration.objects.get(user=request.user)
                return redirect("router")
            except:
                re_obj = RoadRegistration(
                    user=user,
                    road=road,
                    status="n",
                    status_user_state="2",
                    team_or_individual=team_or_individual,
                )
                re_obj.save()

            login(request, user)
            messages.success(request, "اکنون اطلاعات خودرا تکمیل کنید")
            return redirect("account:register2")

        messages.error(request, "اطلاعات وارد شده صحیح نمیباشد!")
        self.context["form"] = form
        return render(request, self.template_name, self.context)


class RegisterLevel2(LoginRequiredMixin, View):
    template_name = "registration/register/level2.html"
    context = {}

    def get(self, request):
        re_obj = RoadRegistration.objects.filter(user=request.user).first()
            
        if int(re_obj.status_user_state) != 2:
            return redirect("router")
        
        self.context["form"] = UserRegisterFormLevel2(instance=request.user)
        return render(request, self.template_name, self.context)

    def post(self, request):
        form_copy = request.POST.copy()
        form_copy.update({
            "birthday": date_db_convertor.jdate_edge_convertor(form_copy["birthday"])
        })

        form = UserRegisterFormLevel2(form_copy, instance=request.user)
        if form.is_valid():
            form.save()
            
            re_obj = RoadRegistration.objects.filter(user=request.user).first()

            if int(re_obj.status_user_state) != 2:
                return redirect("router")
            re_obj.status_user_state = add_one_level(re_obj.status_user_state)
            re_obj.save()

            messages.success(request, "ثبت شد، ادامه دهید.")
            return redirect("account:register3")
        
        messages.error(request, "اطلاعات وارد شده صحیح نمی‌باشد!")
        self.context["form"] = form 
        return render(request, self.template_name, self.context)
    

class RegisterLevel3(LoginRequiredMixin, View):
    template_name = "registration/register/level3.html"
    context = {}

    def get(self, request):
        re_obj = RoadRegistration.objects.filter(user=request.user).first()
            
        if int(re_obj.status_user_state) != 3:
            return redirect("router")

        self.context["form"] = UserRegisterFormLevel3(instance=request.user)
        return render(request, self.template_name, self.context)

    def post(self, request):
        form = UserRegisterFormLevel3(request.POST, instance=request.user)
        if form.is_valid():
            form.save()

            re_obj = RoadRegistration.objects.filter(user=request.user).first()
            
            if int(re_obj.status_user_state) != 3:
                return redirect("router")
            re_obj.status_user_state = add_one_level(re_obj.status_user_state)
            re_obj.save()

            messages.success(request, "به مرحله آخر خوش آمدید.")
            return redirect("account:register4")
        
        messages.error(request, "اطلاعات وارد شده صحیح نمی‌باشد!")
        self.context["form"] = form 
        return render(request, self.template_name, self.context)


class RegisterLevel4(LoginRequiredMixin, View):
    template_name = "registration/register/level4.html"
    context = {}

    def get(self, request):
        re_obj = RoadRegistration.objects.filter(user=request.user).first()
            
        if int(re_obj.status_user_state) != 4:
            return redirect("router")
        
        self.context["form"] = UserRegisterFormLevel4(instance=request.user)
        return render(request, self.template_name, self.context)

    def post(self, request):
        form = UserRegisterFormLevel4(request.POST, instance=request.user)
        if form.is_valid():
            form.save()

            re_obj = RoadRegistration.objects.filter(user=request.user).first()
            
            if int(re_obj.status_user_state) != 4:
                return redirect("router")
            re_obj.status_user_state = add_one_level(re_obj.status_user_state)
            re_obj.complete_registration_date = timezone.datetime.now()
            re_obj.save()

            messages.success(request, "ثبت نام شما به صورت کامل انجام شد.")
            return redirect("account:user-dashboard")
        
        messages.error(request, "اطلاعات وارد شده صحیح نمی‌باشد!")
        self.context["form"] = form 
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
        print(form)
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
        self.context["re_obj"] = RoadRegistration.objects.get(user=request.user)
        return render(request, self.template_name, self.context)
