from django.http import Http404
from django.shortcuts import get_object_or_404

from account.models import User


class CompanyAdminMixin:
    def dispatch(self, request, *args, **kwargs):
        user = get_object_or_404(User, uuid=request.user.uuid)
        if user.is_company or user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise Http404("Access Denied!")


class AcceleratorAdminMixin:
    def dispatch(self, request, *args, **kwargs):
        user = get_object_or_404(User, uuid=request.user.uuid)
        if user.is_center_staff() or user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise Http404("Access Denied!")