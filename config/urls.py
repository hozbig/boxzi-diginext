from django.contrib import admin
from django.urls import include, path
from django.shortcuts import redirect, render
from django.http import Http404
from django.conf import settings
from django.contrib.auth.decorators import login_required


def router(request):
    user = request.user

    if not user.is_authenticated:
        return redirect("account:login-or-register")
    
    if user.is_superuser or user.is_staff:
        return redirect("admin:index")
    elif user.is_team_member:
        return redirect("account:user-dashboard")
    elif user.is_mentor:
        return redirect("account:mentor-dashboard")
    elif user.is_investor:
        return redirect("investor:dashboard")
    elif user.is_company:
        return redirect("company:dashboard")
    elif user.is_center_staff():
        return redirect("company:acc-dashboard")
    else:
        raise Http404("You do not have valid permissions!")


@login_required
def under_maintenance(request):
    return render(request, "under_maintenance.html", {})


@login_required
def forbidden(request, *args, **kwargs):
    return render(request, "forbidden.html", {})


urlpatterns = [
    path('admin/', admin.site.urls),
    path("", router, name="router"),
    path("under-maintenance", under_maintenance, name="under-maintenance"),
    path('accounts/', include('account.urls')),
    path('content/', include('content.urls')),
    path('company/', include('company.urls')),
    path('quiz/', include('quiz.urls')),
    path('plan/', include('plan.urls')),
    path('team/', include('team.urls')),
    path('investor/', include('investor.urls')),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)