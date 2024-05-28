from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import View, UpdateView, ListView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from content.models import Road
from plan.models import Plan

from .forms import  InvestorFoundCreationForm, InvestorFoundUpdateForm
from .models import InvestorFound


class InvestorDashboard(LoginRequiredMixin, View):
    template_name = "investor/dashboard.html"
    context = {"title":"داشبورد سرمایه گذار"}

    def get(self, request):
        return render(request, self.template_name, self.context)


class FundsManagements(LoginRequiredMixin, View):
    template_name = "investor/funds-management.html"
    form_class = InvestorFoundCreationForm
    context = {"title":"مدیریت صندوق ها"}

    def get(self, request):
        self.context["fund_form"] = self.form_class
        return render(request, self.template_name, self.context)
    
    def post(self, request):
        if request.method == 'POST':
            form = self.form_class(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "عملیات با موفقیت انجام شد")
            else:
                messages.error(request, "مشکلی در فرم وجود دارد!")
        else:
            messages.error(request, "درخاست نامعتبر!")
        return redirect(reverse('investor:funds-management'))


class UpdateFund(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = InvestorFound
    template_name = "investor/update-fund.html"
    form_class = InvestorFoundUpdateForm
    success_message = "عملیات با موفقیت انجام شد"
    slug_field, slug_url_kwarg = "uuid", "uuid"

    def get_success_url(self, **kwargs):         
        return reverse_lazy('investor:update-fund', args = (self.object.uuid,))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "ویرایش صندوق"
        return context
    

@login_required
def delete_fund(request, uuid):
    try:
        InvestorFound.objects.get(uuid=uuid).delete()
        messages.success(request, "عملیات با موفقیت انجام شد")
    except:
        messages.error(request, "درخاست نامعتبر!")

    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


class RoadList(LoginRequiredMixin, ListView):
    model = Road
    template_name = "investor/roads.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "لیست برنامه های فعال"
        return context


class RoadInvestment(LoginRequiredMixin, View):
    template_name = "investor/road-investment.html"
    context = {"title": "سرمایه گذاری برروی برنامه"}

    def get(self, request, uuid):
        obj = Road.objects.get(uuid=uuid)
        self.context["object"] = obj
        return render(request, self.template_name, self.context)


class ProductList(LoginRequiredMixin, ListView):
    model = Plan
    template_name = "investor/product-list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "لیست برنامه های فعال"
        return context


class ProductInvestment(LoginRequiredMixin, View):
    template_name = "investor/product-investment.html"
    context = {"title": "سرمایه گذاری برروی محصول"}

    def get(self, request, uuid):
        obj = Plan.objects.get(uuid=uuid)
        self.context["object"] = obj
        return render(request, self.template_name, self.context)