import logging
from django.shortcuts import redirect, get_object_or_404, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView, View, ListView
from itertools import chain
from team.models import RoadRegistration

from .models import Content, WatchedContent, Road

logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

class Roads(LoginRequiredMixin, View):
    template_name = "content/roads.html"
    context = {"title":"مسیرآموزشی"}

    def get(self, request):
        user = request.user
        registration_obj = user.user_of_road_registration.first()
        if not registration_obj.status_user_state == "5":
            return redirect("router")
        
        try:
            road = registration_obj.road
        except:
            road = Road.objects.first()

        task = road.pre_register_task
        task_business_side = road.pre_register_task_for_business_side

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

        self.context["object"] = Road.objects.first()
        self.context["registration_obj"] = request.user.user_of_road_registration.first()
        return render(request, self.template_name, self.context)
    

class RoadDetail(LoginRequiredMixin, DetailView):
    model = Road
    template_name = "content/road.html"
    slug_field, slug_url_kwarg = "uuid", "uuid"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "مسیر آموزشی"
        context["watched_list"] = WatchedContent.objects.filter(user=self.request.user).values_list('content__uuid', flat=True)

        collections = self.get_object().road_of_collection_order.all()
        steps = []
        for col_ord in collections:
            contents = col_ord.collection.collection_of_content_order.all()
            exams = col_ord.collection.collection_of_exam_order.all()
            tasks = col_ord.collection.collection_of_task_order.all()
            collection_steps = sorted(chain(contents, exams, tasks), key=lambda x: x.row_number)
            steps.extend(collection_steps)
        context["collections"] = collections
        context["steps"] = sorted(steps, key=lambda x: x.row_number)
        context["steps"] = steps
        return context


class ContentDetail(LoginRequiredMixin, DetailView):
    model = Content
    template_name = "content/detail.html"
    slug_field, slug_url_kwarg = "uuid", "uuid"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = f"{self.get_object().title}"
        return context


@login_required
def user_watched_content(request, content_uuid):
    content = get_object_or_404(Content, uuid=content_uuid)
    WatchedContent.objects.create(user=request.user, content=content)

    if content.medals:
        request.user.received_medals = (request.user.received_medals or 0) + content.medals
        request.user.save()

    return redirect("content:roads")


class FundsManagements(LoginRequiredMixin, View):
    template_name = "content/funds-management.html"
    context = {"title":"مدیریت صندوق ها"}

    def get(self, request):
        return render(request, self.template_name, self.context)
