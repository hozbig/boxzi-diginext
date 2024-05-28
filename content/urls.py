from django.urls import path
from . import views

app_name = "content"
urlpatterns = [
    path("roads/", views.Roads.as_view(), name="roads"),
    path("road-detail/<str:uuid>/", views.RoadDetail.as_view(), name="road-detail"),
    path("<str:uuid>/detail/", views.ContentDetail.as_view(), name="detail"),
    path("watched-content/<str:content_uuid>", views.user_watched_content, name="watched-content"),
    path("funds/management/", views.FundsManagements.as_view(), name="funds-management"),
]