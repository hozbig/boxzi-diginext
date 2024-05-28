from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.urls import reverse
from django.contrib.auth import login
from content.models import WatchedContent
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from utils import date_db_convertor
from django.contrib import messages
from django.http import HttpResponseRedirect

from .models import User, WorkExperience, LeanCanvas
from .forms import (
    CustomUserChangeForm,
    MeetingCreateForm,
    UserRegisterFormLevel1,
    UserRegisterFormLevel2,
    UserLoginOrRegisterForm,
    WorkExperienceCreateForm
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
            messages.success(request, "اطلاعات شما دریافت شد")
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
            messages.success(request, "تبریک! ثبت‌نام شما انجام شد.")
            return redirect("router")
        
        messages.error(request, "اطلاعات وارد شده صحیح نمی‌باشد!")
        self.context["form"] = form 
        return render(request, self.template_name, self.context)
    

class ChangeUser(LoginRequiredMixin, ChangeUserAccessMixin, View):
    form_class = CustomUserChangeForm
    template_name = "account/change-user.html"
    success_message = "پروفایل شما با موفقیت ویرایش شد."
    context = {"title": "ویرایش کاربر"}

    def get(self, request, username):
        user = User.objects.get(username=username)
        self.context["object"] = user
        self.context["form"] = self.form_class(instance=user)
        # self.context["experience_form"] = WorkExperienceCreateForm

        return render(request, self.template_name, self.context)

    def post(self, request, username):
        user = User.objects.get(username=username)

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


class MentorList(LoginRequiredMixin, ListView):
    model = User
    template_name = "account/mentor/list.html"

    def get_queryset(self) -> QuerySet:
        queryset = super().get_queryset()
        return queryset.filter(is_mentor=True)
    
    def get_context_data(self, **kwargs) -> dict[str]:
        context = super().get_context_data(**kwargs)
        context["title"] = "لیست مربی ها"
        return context


class MentorDashboard(LoginRequiredMixin, View):
    template_name = "account/mentor/dashboard.html"
    context = {}

    def get(self, request):
        self.context["title"] = f"داشبورد مربی {request.user.get_full_name()}"
        self.context["object"] = request.user
        return render(request, self.template_name, self.context)
    

class MentorProfile(LoginRequiredMixin, View):
    template_name = "account/mentor/profile.html"
    context = {}

    def get(self, request, username):
        user = User.objects.get(username=username)
        self.context["title"] = "پروفایل مربی"
        self.context["object"] = user
        self.context["meeting_form"] = MeetingCreateForm
        return render(request, self.template_name, self.context)


@login_required
@require_POST
def new_meeting_session(request):
    if request.method == "POST":
        form_copy = request.POST.copy()
        form_copy.update(
            {
                "date": date_db_convertor.jdate_edge_convertor(form_copy["date"]),
                "team_member": request.user.id,
                "team": request.user.members_of_team.first().id,
            }
        )

        form = MeetingCreateForm(form_copy)

        if form.is_valid():
            form.save()
            messages.success(request, "درخواست جلسه شما با موفقیت ثبت شد")
        else:
            messages.error(request, "مشکلی در فرم وجود دارد!")
    else:
        messages.error(request, "درخاست نامعتبر!")
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


@login_required
@require_POST
def save_work_experiences(request):
    if request.method == "POST":
        form_copy = request.POST.copy()
        form_copy.update(
                {
                    "from_date": date_db_convertor.jdate_edge_convertor(form_copy["from_date"]),
                    "to_date": date_db_convertor.jdate_edge_convertor(form_copy["to_date"]),
                    "user": request.user,
                }
            )
        
        print(form_copy)
        # TODO: I got this error while form validation:
        # The "f" value cannot be selected
        form = WorkExperienceCreateForm(form_copy, instance=request.user)
        print(form)
        if form.is_valid():
            form.save()
            messages.success(request, "عملیات با موفقیت انجام شد")
        else:
            messages.error(request, "مشکلی در فرم وجود دارد!")
    else:
        messages.error(request, "درخاست نامعتبر!")
    return redirect(reverse('account:update', kwargs={'username': request.user.username}))


def lean_canvas(request):
    return render(request, 'account/lean-canvas.html', {})


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def save_lean_canvas(request):
    if request.method == 'POST':
        try:
            data = request.POST.get("json_data")
            
            print("--------------------------")
            print(data)
            # Create a new object with the data
            obj = LeanCanvas.objects.create(
                data=data,
            )

            # Save the object
            obj.save()

            # Return success response
            return JsonResponse({'message': 'Canvas created successfully'}, status=201)
        except Exception as e:
            # Return error response if something goes wrong
            return JsonResponse({'error': str(e)}, status=400)
    else:
        # Return method not allowed if request method is not POST
        return JsonResponse({'error': 'Method not allowed'}, status=405)
