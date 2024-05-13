from django.http import HttpResponse
from base import models
from base import api
from django_multitenant.utils import get_current_tenant, set_current_tenant
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed


# 'Droid Sans Mono', 'monospace', monospace
class CollegeMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        user = get_user_from_request(request)

        if user:
            tenant_obj = get_tenant_from_user(user)
            set_current_tenant(tenant_obj)
            return self.get_response(request)

        return HttpResponse("Nice Try, now hit with valid user details")  
        


def get_tenant_from_user(user):
    return models.Student.objects.get(user=user).college

def get_user_from_request(request):
    token_value = request.headers.get("Authorization", "")

    auth_instance = JWTAuthentication() 
    try:
        user_auth_tuple = auth_instance.authenticate(request)
    except AuthenticationFailed:
        return None
    if not user_auth_tuple:
        return None
    return user_auth_tuple[0]