from django.contrib.auth import views as user_views
from django.urls import path
from . import views

app_name = "account"
urlpatterns = [
    path("login/", user_views.LoginView.as_view(), name="login"),
    path("logout/", user_views.LogoutView.as_view(), name="logout"),
    # path('password_change/', user_views.PasswordChangeView.as_view(), name='password_change'),
    # path('password_change/done/', user_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    # path('password_reset/', user_views.PasswordResetView.as_view(), name='password_reset'),
    # path('password_reset/done/', user_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    # path('reset/<uidb64>/<token>/', user_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('reset/done/', user_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('<str:username>/update/', views.ChangeUser.as_view(), name='update'),

    path("login-or-register/", views.LoginOrRegister.as_view(), name="login-or-register"),
    path("register/", views.RegisterLevel1.as_view(), name="register"),
    path("register/level=2", views.RegisterLevel2.as_view(), name="register2"),

    # ======== Target-User(team_member) Urls ========
    path("", views.UserDashboard.as_view(), name="user-dashboard"),

    # ======== Mentor Urls ========
    path("mentor/list/", views.MentorList.as_view(), name="mentor-list"),
    path("mentor/", views.MentorDashboard.as_view(), name="mentor-dashboard"),
    path("mentor/<str:username>/", views.MentorProfile.as_view(), name="mentor-profile"),

    path("meeting/new/", views.new_meeting_session, name="new-meeting-session"),
    path("work-experience/new/", views.save_work_experiences, name="new-work-experience"),
    path("lean-canvas/", views.lean_canvas, name="lean-canvas"),
    path('lean-canvas/create/', views.save_lean_canvas, name='lean-canvas-create'),
    
]