from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.contrib import messages
from django.views.generic import View, DetailView, UpdateView
from subject.models import Topic
from account.templatetags.tag_library import get_topics_and_counts
from account.models import User
from content.models import Road
from plan.models import Plan
from plan.forms import PlanCreateForm
from django.contrib.auth.hashers import make_password
from django.utils.crypto import get_random_string

from .models import RoadRegistration, StartUpTeam, TeamMember, search_items
from .mixins import TeamAccessMixin
from .forms import RoadRegistrationForm, StartUpTeamForm, TeamMemberForm, ExtraDaysForCompleteRegistration


class TeamDashboard(LoginRequiredMixin, TeamAccessMixin, View):
    template_name = "team/dashboard.html"
    context = {
        "title":"داشبورد تیم",
        "object":None,
    }

    def get(self, request):
        # This condition checks whether the user has the required permissions of a team member or not
        if request.user.members_of_team.first():
            object = request.user.members_of_team.first()
            self.context["title"] = f"داشبورد تیم {request.user.members_of_team.first().name}"
            self.context["object"] = object
            self.context["topics"] = Topic.objects.all()
            self.context["topics_and_counts"] = get_topics_and_counts(object.uuid)
        return render(request, self.template_name, self.context)
    

class TeamProfile(LoginRequiredMixin, DetailView):
    model = StartUpTeam
    template_name = "team/profile.html"
    slug_field, slug_url_kwarg = "uuid", "uuid"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = f"پروفایل تیم" 
        return context
    

class CreateTeam(LoginRequiredMixin, View):
    model = StartUpTeam
    form_class = StartUpTeamForm
    template_name = "team/manage-teams.html"
    context = {"title": "ساخت تیم"}

    def get(self, request):
        self.context["form"] = self.form_class
        self.context["teams"] = request.user.user_of_team_member.filter(is_coordinator=True)
        return render(request, self.template_name, self.context)
    
    def post(self, request):
        user = request.user
        form = request.POST
        form = self.form_class(form)
        
        if form.is_valid():
            registration_obj = request.user.user_of_road_registration.first()

            if request.user.user_of_team_member.first() or registration_obj.team_or_individual == "i":
                return redirect("router")

            obj = form.save()
            team_member = TeamMember(
                team=obj,
                user=user,
                is_coordinator=True,
                is_owner=True,
            )
            team_member.save()
            
            registration_obj.team = obj
            registration_obj.save()
            
            messages.success(request, "عملیات با موفقیت انجام شد")
            default_redirect_url = reverse('team:update-team', args=[obj.uuid])
            next_url = request.GET.get('next')
            if next_url:
                default_redirect_url += f'?next={next_url}'
            return redirect(default_redirect_url)
        messages.error(request, "مشکلی در فرم وجود دارد!")
        self.context["form"] = form
        self.context["teams"] = request.user.user_of_team_member.filter(is_coordinator=True)
        return render(request, self.template_name, self.context)

    
class UpdateTeam(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = StartUpTeam
    form_class = StartUpTeamForm
    template_name = "team/update-team.html"
    success_message = "عملیات با موفقیت انجام شد"
    slug_field, slug_url_kwarg = "uuid", "uuid"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "ویرایش تیم"

        # Check for form errors and data in session
        form_errors = self.request.session.pop('form_errors', None)
        form_data = self.request.session.pop('form_data', None)
        if form_errors and form_data:
            add_member_form = TeamMemberForm(data=form_data)
            add_member_form.errors.update(form_errors)
        else:
            add_member_form = TeamMemberForm()

        context["add_product_form"] = PlanCreateForm
        context["add_member_form"] = add_member_form
        context["next_url"] = self.request.GET.get('next', None)
        return context
    
    def get_success_url(self, **kwargs):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        return reverse_lazy('team:update-team', args = (self.object.uuid,))
    

@login_required
@require_POST
def save_team_member(request):
    if request.method == 'POST':
        form = TeamMemberForm(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data["phone_number"]
            email = form.cleaned_data["email"]
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            user_objects = User.objects.filter(phone_number=phone_number)
            if not user_objects.exists():
                # generated_pass is the password can login with it
                generated_pass = get_random_string(length=10)
                hashed_password = make_password(generated_pass)
                user_obj = User.objects.create(
                    phone_number = phone_number,
                    email = email,
                    first_name = first_name,
                    last_name = last_name,
                    password = hashed_password,
                    is_team_member = True
                )
                registration_obj = RoadRegistration(
                    team = request.user.user_of_road_registration.first().team,
                    user = user_obj,
                    road = request.user.user_of_road_registration.first().road,
                    status = "n",
                    status_user_state = "2",
                    team_or_individual = "a"
                )
                registration_obj.save()
                TeamMember.objects.create(
                    team = request.user.user_of_team_member.first().team,
                    user = user_obj,
                )
            else:
                messages.error(request, "این کاربر از قبل ثبت نام کرده است، امکان اضافه کردن آن به تیم خود وجود ندارد!")
                return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
            messages.success(request, "عملیات با موفقیت انجام شد")
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
        else:
            # Store form errors and data in session
            request.session['form_errors'] = form.errors
            request.session['form_data'] = request.POST
            messages.error(request, "مشکلی در فرم وجود دارد!")
    else:
        messages.error(request, "درخواست نامعتبر!")
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


@login_required
def delete_team_member(request, uuid, team_uuid):
    try:
        team = StartUpTeam.objects.get(uuid=team_uuid)
        requesting_user = team.team_of_team_member.get(user=request.user)
    except (StartUpTeam.DoesNotExist, TeamMember.DoesNotExist):
        messages.error(request, "عضو مورد نظر پیدا نشد یا شما دسترسی لازم برای انجام این عملیات را ندارید!")
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

    if not requesting_user.is_owner:
        messages.error(request, "شما دسترسی لازم برای انجام این عملیات را ندارید!")
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

    try:
        obj = TeamMember.objects.get(uuid=uuid)
    except TeamMember.DoesNotExist:
        messages.error(request, "عضو مورد نظر پیدا نشد!")
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

    if obj.uuid == requesting_user.uuid or obj.is_owner:
        messages.error(request, "نمیتوانید خودتان یا فرد سازنده تیم را حذف کنید!")
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

    obj.delete()
    messages.success(request, "عملیات با موفقیت انجام شد")
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
    

class RoadRegistrationView(LoginRequiredMixin, View):
    template_name = "team/road-registration.html"
    model = RoadRegistration
    form_class = RoadRegistrationForm
    context = {"title": "ثبت نام برنامه آموزشی"}

    def get(self, request, uuid):
        obj = Road.objects.get(uuid=uuid)

        try:
            self.context["is_register"] = RoadRegistration.objects.get(user=request.user, road=obj)
        except:
            self.context["is_register"] = False

        self.context["object"] = obj
        self.context["form"] = self.form_class
        return render(request, self.template_name, self.context)

    def post(self, request, uuid):
        user = request.user
        road = Road.objects.get(uuid=uuid)
        
        registration_obj = RoadRegistration.objects.filter(road=road, user=request.user).first()

        if registration_obj.status != "n":
            return redirect("router")

        if registration_obj.team_or_individual == "t" and user.user_of_team_member.first().is_owner and registration_obj.team.all_users_completed_registration():
            registration_obj.status = "w"
            registration_obj.client_last_response_date = timezone.datetime.now()
            registration_obj.save()
            messages.success(request, "درخواست شما ثبت شد")
            messages.info(request, "درخواست شما برای شرکت تیمتان در این مسیر رشد با موقیت ثبت شد.")
            return redirect("router")
        elif registration_obj.team_or_individual == "i" and registration_obj.is_complete_registration_for_individual():
            registration_obj.status = "w"
            registration_obj.client_last_response_date = timezone.datetime.now()
            registration_obj.save()
            messages.success(request, "درخواست شما ثبت شد")
            messages.info(request, "درخواست شما برای شرکت انفرادی در این مسیر رشد با موقیت ثبت شد.")
            return redirect("router")
        else:
            messages.error(request, "شما دسترسی لازم برای انجام این عملیات را ندارید!")
            return redirect("router")


class RegistrationDetail(LoginRequiredMixin, View):
    template_name = "team/registration-detail.html"
    model = RoadRegistration
    form_class = RoadRegistrationForm
    context = {"title": "مشاهده درخواست"}

    def get(self, request, uuid):
        obj = RoadRegistration.objects.get(uuid=uuid)

        if obj.status == "w":
            obj.status = "p"
            obj.save()
            messages.info(request, "وضعیت مشاهده شده برای این درخواست ثبت شد")

        self.context["object"] = obj
        
        return render(request, self.template_name, self.context)


@login_required
def watch_registration(request, uuid):
    obj = RoadRegistration.objects.get(uuid=uuid)
    if obj.status == "p":
        messages.error(request, "عملیات تکراری")
        return redirect(reverse('company:team-management'))
    obj.status = "p"
    obj.save()
    messages.success(request, "عملیات با موفقیت انجام شد")
    return redirect(reverse('company:team-management'))


@login_required
def reject_registration(request, uuid):
    obj = RoadRegistration.objects.get(uuid=uuid)
    if obj.status == "r":
        messages.error(request, "عملیات تکراری")
        return redirect(reverse('company:team-management'))
    obj.status = "r"
    obj.save()
    messages.success(request, "عملیات با موفقیت انجام شد")
    return redirect(reverse('company:team-management'))


@login_required
def approve_registration(request, uuid):
    obj = RoadRegistration.objects.get(uuid=uuid)
    if obj.status == "a":
        messages.error(request, "عملیات تکراری")
        return redirect(reverse('company:team-management'))
    obj.status = "a"
    obj.save()
    messages.success(request, "عملیات با موفقیت انجام شد")
    return redirect(reverse('company:team-management'))


class FundsManagements(LoginRequiredMixin, View):
    template_name = "team/funds-management.html"
    context = {"title":"مدیریت صندوق ها"}

    def get(self, request):
        return render(request, self.template_name, self.context)


class IdeaManagements(LoginRequiredMixin, View):
    template_name = "team/idea-management.html"
    context = {"title":"مدیریت ایده ها"}

    def get(self, request):
        return render(request, self.template_name, self.context)


class ProductManagements(LoginRequiredMixin, View):
    template_name = "team/product-management.html"
    model = Plan
    form_class = PlanCreateForm
    context = {"title":"مدیریت محصولات ها"}

    def get(self, request):
        self.context["form"] = self.form_class
        return render(request, self.template_name, self.context)
    
    def post(self, request):
        form_copy = request.POST.copy()
        form_copy.update({"user": request.user,})

        form = self.form_class(form_copy, request.FILES)
        print(form)
        if form.is_valid():
            form.save()
            messages.success(request, "محصول شما موفقیت ثبت شد")
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
        
        messages.error(request, "مشکلی پیش آمده است!")
        self.context["form"] = self.form_class(request.POST)
        return render(request, self.template_name, self.context)


class AddProduct(LoginRequiredMixin, View):
    template_name = "team/add-product.html"
    model = Plan
    form_class = PlanCreateForm
    context = {"title":"مدیریت ایده/محصول"}

    def get(self, request):
        self.context["form"] = self.form_class
        return render(request, self.template_name, self.context)
    
    def post(self, request):
        if request.user.user_of_plan.first():
            return redirect("router")
        
        # team = request.POST.get("team")
        form_copy = request.POST.copy()
        form_copy.update({"user": request.user,})

        form = self.form_class(form_copy, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "محصول شما با موفقیت ثبت شد")
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
        
        messages.error(request, "مشکلی پیش آمده است!")
        self.context["form"] = form
        return render(request, self.template_name, self.context)


@require_POST
def save_product(request):
    if request.user.user_of_plan.first():
        return redirect("router")
    
    context = {"title":"مدیریت ایده/محصول"}
    # team = request.POST.get("team")
    form_copy = request.POST.copy()
    # has_mvp = request.POST.get("has_mvp")
    # if has_mvp in "01":
    #     has_mvp = has_mvp == 1
    # form_copy.update({"user": request.user, "has_mvp": has_mvp})
    form_copy.update({"user": request.user,})

    form = PlanCreateForm(form_copy, request.FILES)
    print(form)
    if form.is_valid():
        form.save()
        messages.success(request, "محصول شما با موفقیت ثبت شد")
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

    messages.error(request, "مشکلی پیش آمده است!")
    request.session['form_errors'] = form.errors
    request.session['form_data'] = request.POST
    context["form"] = form
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


@require_POST
def save_extra_day_for_complete_registraion(request):
    form = ExtraDaysForCompleteRegistration(request.POST)
    
    if form.is_valid():
        uuid = form.cleaned_data["registration_object_uuid"]
        days = form.cleaned_data["extra_days"]

        registration_object = RoadRegistration.objects.get(uuid=uuid)
        registration_object.validity_pride_days += days
        registration_object.save()
        messages.success(request, "عملیات مورد نظر با موفقیت انجام شد")
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
    messages.success(request, "خطا در انجام عملیات!")
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


# This functions dont need any authentication
# searchzi: search + boxzi
# this is a outside template of another function
def searchzi(request):
    query = request.GET.get('q')
    result = None
    if query:
        result = search_items(query)
    return render(request, 'team/searchZi.html', {'result': result, 'query': query})

def search_iframe(request):
    query = request.GET.get('q')
    result = None
    if query:
        result = search_items(query)
    return render(request, 'team/search-iframe.html', {'result': result, 'query': query})



from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Category
@csrf_exempt
def create_team(request):
    if request.method == 'POST':
        try:
            name = request.POST.get("name")
            description = request.POST.get("description")
            cat_name = request.POST.get("cat_name")

            try:
                cat = Category.objects.get(name=cat_name)
            except:
                cat = Category.objects.create(
                    name = cat_name
                )
                cat.save()

            try:
                StartUpTeam.objects.get(name=name)
                return JsonResponse({'message': 'Team Was Exist'}, status=201)
            except:
                team = StartUpTeam.objects.create(
                    name=name,
                    status="i",
                    description=description,
                    category=cat
                )

            # Save the team object
            team.save()

            # Return success response
            return JsonResponse({'message': 'Team created successfully'}, status=201)
        except Exception as e:
            # Return error response if something goes wrong
            return JsonResponse({'error': str(e)}, status=400)
    else:
        # Return method not allowed if request method is not POST
        return JsonResponse({'error': 'Method not allowed'}, status=405)