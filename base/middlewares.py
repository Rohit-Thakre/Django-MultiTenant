from django.http import HttpResponse
from base import models
from base import api
from django_multitenant.utils import get_current_tenant, set_current_tenant


# 'Droid Sans Mono', 'monospace', monospace
class CollegeMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        user = request.user
    
        if request.user and not request.user.is_anonymous:
            tenant_obj = get_tenant_from_user(user)
            set_current_tenant(tenant_obj)
            # print(get_current_tenant())
           
        
        return self.get_response(request)


def get_tenant_from_user(user):
    return models.Student.objects.get(user=user).college