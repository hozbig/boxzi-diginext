from django.http import Http404
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect

from account.models import User


class ChangeUserAccessMixin:
    def dispatch(self, request, uuid, *args, **kwargs):
        user = get_object_or_404(User, uuid=uuid)
        if user == request.user or request.user.is_superuser:
            return super().dispatch(request, uuid, *args, **kwargs)
        else:
            raise Http404("Access Denied!")


class AdminAccessMixin:
    def dispatch(self, request, *args, **kwargs):
        user = get_object_or_404(User, id=request.user.id)
        if user.is_staff or user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise Http404("Access Denied!")


class AnonymousRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('router')
        return super().dispatch(request, *args, **kwargs)