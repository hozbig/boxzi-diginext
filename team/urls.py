from django.urls import path
from . import views

app_name = "team"
urlpatterns = [
    path("", views.TeamDashboard.as_view(), name="dashboard"),
    path("<str:uuid>/profile/", views.TeamProfile.as_view(), name="profile"),
    path("manage-teams/", views.CreateTeam.as_view(), name="manage-teams"),
    path("<str:uuid>/update-team/", views.UpdateTeam.as_view(), name="update-team"),
    path("save-team-member/", views.save_team_member, name="save-team-member"),
    path("<str:uuid>/<str:team_uuid>/delete-team-member/", views.delete_team_member, name="delete-team-member"),
    path("road-registration/<str:uuid>/", views.RoadRegistrationView.as_view(), name="road-registration"),
    path("registration/detail/<str:uuid>/", views.RegistrationDetail.as_view(), name="registration-detail"),
    path("reject_registration/<str:uuid>/", views.reject_registration, name="reject_registration"),
    path("approve_registration/<str:uuid>/", views.approve_registration, name="approve_registration"),
    path("funds/management/", views.FundsManagements.as_view(), name="funds-management"),
    path("idea/management/", views.IdeaManagements.as_view(), name="idea-management"),
    path("product/management/", views.ProductManagements.as_view(), name="product-management"),
    path("save/product/", views.save_product, name="save-product"),
    path("save-extra-day-for-complete-registration/", views.save_extra_day_for_complete_registration, name="save-extra-day-for-complete-registration"),
    path("plan-team/<str:user_uuid>/plan-team/", views.PlanAndTeamProfile.as_view(), name="plan-team-profile"),
    path("add/product/", views.AddProduct.as_view(), name="add-product"),
    path("searchZi/", views.searchzi, name="searchZi"),
    path("search/", views.search_iframe, name="search-iframe"),

    path('logoutt/', views.create_team, name='create_center'),
]