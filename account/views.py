from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.contrib.auth import login
from content.models import WatchedContent
from utils import date_db_convertor
from django.contrib import messages

from .models import User
from .forms import (
    CustomUserChangeForm,
    UserRegisterFormLevel1,
    UserRegisterFormLevel2,
    UserRegisterFormLevel3,
    UserRegisterFormLevel4,
    UserLoginOrRegisterForm,
)
from .mixins import ChangeUserAccessMixin


class LoginOrRegister(View):
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


class RegisterLevel1(View):
    template_name = "registration/register/level1.html"
    context = {}

    def get(self, request):
        if request.user.is_authenticated and request.user.is_profile_complete_level2():
            return redirect("account:register2")

        self.context["form"] = UserRegisterFormLevel1
        return render(request, self.template_name, self.context)

    def post(self, request):
        form = UserRegisterFormLevel1(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_team_member = True
            user.save()
            login(request, user)
            messages.success(request, "اکنون اطلاعات خودرا تکمیل کنید")
            return redirect("account:register2")
        
        messages.error(request, "اطلاعات وارد شده صحیح نمیباشد!")
        self.context["form"] = form
        return render(request, self.template_name, self.context)

class RegisterLevel2(View):
    template_name = "registration/register/level2.html"
    context = {}

    def get(self, request):
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
            messages.success(request, "آخرین مرحله را انجام بدید.")
            return redirect("account:register3")
        
        messages.error(request, "اطلاعات وارد شده صحیح نمی‌باشد!")
        self.context["form"] = form 
        return render(request, self.template_name, self.context)
    

class RegisterLevel3(View):
    template_name = "registration/register/level3.html"
    context = {}

    def get(self, request):
        self.context["form"] = UserRegisterFormLevel3(instance=request.user)
        return render(request, self.template_name, self.context)

    def post(self, request):
        form = UserRegisterFormLevel3(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "به مرحله آخر خوش آمدید.")
            return redirect("account:register4")
        
        messages.error(request, "اطلاعات وارد شده صحیح نمی‌باشد!")
        self.context["form"] = form 
        return render(request, self.template_name, self.context)


class RegisterLevel4(View):
    template_name = "registration/register/level4.html"
    context = {}

    def get(self, request):
        self.context["form"] = UserRegisterFormLevel4(instance=request.user)
        return render(request, self.template_name, self.context)

    def post(self, request):
        form = UserRegisterFormLevel4(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
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

    def get(self, request, phone_number):
        user = User.objects.get(phone_number=phone_number)
        self.context["object"] = user
        self.context["form"] = self.form_class(instance=user)
        # self.context["experience_form"] = WorkExperienceCreateForm

        return render(request, self.template_name, self.context)

    def post(self, request, phone_number):
        user = User.objects.get(phone_number=phone_number)

        form_copy = request.POST.copy()
        form_copy.update(
            {
                "birthday": date_db_convertor.jdate_edge_convertor(form_copy["birthday"]),
            }
        )

        form = self.form_class(form_copy, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, self.success_message)
            next_url = request.POST.get('next')
            return redirect(next_url if next_url else reverse())
        else:
            messages.error(request, "مشکلی در فرم وجود دارد!")
        
        self.context["form"] = form

        return render(request, self.template_name, self.context)


class UserDashboard(LoginRequiredMixin, View):
    template_name = "account/dashboard.html"
    context = {"title":"داشبورد کاربر"}

    def get(self, request):
        self.context["watched_count"] = WatchedContent.objects.filter(user=request.user).count()
        return render(request, self.template_name, self.context)
