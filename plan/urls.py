from django.urls import path
from . import views
from config.urls import forbidden

app_name = "plan"
urlpatterns = [
    path("create/", views.CreatePlan.as_view(), name="create"),
    path("<str:uuid>/profile/", views.TeamProductProfile.as_view(), name="profile"),
    path("<str:uuid>/detail/", views.PlanDetail.as_view(), name="detail"),
]
