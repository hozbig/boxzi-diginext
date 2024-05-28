from django.http import Http404
from django.shortcuts import get_object_or_404

from account.models import User


class ChangeUserAccessMixin:
    def dispatch(self, request, username, *args, **kwargs):
        user = get_object_or_404(User, username=username)
        if user == request.user or request.user.is_superuser:
            return super().dispatch(request, username, *args, **kwargs)
        else:
            raise Http404("Access Denied!")


class AdminAccessMixin:
    def dispatch(self, request, *args, **kwargs):
        user = get_object_or_404(User, id=request.user.id)
        if user.is_staff or user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise Http404("Access Denied!")
