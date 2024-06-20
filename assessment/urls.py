from django.contrib.auth import views as user_views
from django.urls import path
from . import views

app_name = "assessment"
urlpatterns = [
    path("question/create/", views.CreateQuestion.as_view(), name="create-question"),
]