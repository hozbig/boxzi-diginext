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
    path('<str:uuid>/update/', views.ChangeUser.as_view(), name='update'),

    path("login-or-register/", views.LoginOrRegister.as_view(), name="login-or-register"),
    path("register/", views.RegisterLevel1.as_view(), name="register"),
    path("register/level=2", views.RegisterLevel2.as_view(), name="register2"),
    path("register/level=3", views.RegisterLevel3.as_view(), name="register3"),
    path("register/level=4", views.RegisterLevel4.as_view(), name="register4"),

    # ======== Target-User(team_member) Urls ========
    path("", views.UserDashboard.as_view(), name="user-dashboard"),
    
]