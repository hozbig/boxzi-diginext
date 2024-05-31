from django.urls import reverse, reverse_lazy
from django.shortcuts import redirect
from django.views.generic import CreateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages

from .models import Plan
from .forms import PlanCreateForm


class CreatePlan(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Plan
    form_class = PlanCreateForm
    template_name = 'plan/create.html'
    success_url = reverse_lazy("plan:create")
    success_message = "ایده شما با موفقیت ثبت شد"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = f"ثبت ایده"
        return context


class TeamProductProfile(LoginRequiredMixin, DetailView):
    model = Plan
    template_name = "plan/profile.html"
    slug_field, slug_url_kwarg = "uuid", "uuid"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = f"پروفایل محصول" 
        return context
    

class PlanDetail(LoginRequiredMixin, DetailView):
    model = Plan
    template_name = "plan/detail.html"
    slug_field, slug_url_kwarg = "uuid", "uuid"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = self.get_object()
        liked = False

        if obj.likes.filter(id=self.request.user.id).exists():
            liked = True

        context['number_of_likes'] = obj.number_of_likes()
        context['post_is_liked'] = liked
        return context


@login_required
def plan_like_unlike(request, uuid):
    try:
        plan = Plan.objects.get(uuid=uuid)
    except Plan.DoesNotExist:
        messages.error(request, "ایده یا محصولی پیدا نشد!")
        return redirect(reverse('plan:detail', kwargs={'uuid': uuid}))

    if plan.likes.filter(id=request.user.id).exists():
        plan.likes.remove(request.user)
    else:
        plan.likes.add(request.user)

    messages.success(request, "عملیات با موفقیت انجام شد")
    return redirect(reverse('plan:detail', kwargs={'uuid': uuid}))
