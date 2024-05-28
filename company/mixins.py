from django.http import Http404
from django.shortcuts import get_object_or_404

from account.models import User


class CompanyAdminMixin:
    def dispatch(self, request, *args, **kwargs):
        user = get_object_or_404(User, id=request.user.id)
        if user.is_company_staff() or user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise Http404("Access Denied!")
