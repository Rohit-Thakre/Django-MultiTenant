from django.shortcuts import HttpResponse
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from base import models
from django_multitenant.utils import set_current_tenant,get_current_tenant
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


class SetTenantModel:
    permission_classes = [IsAuthenticated]
    def __init__(self, organisation):
        self.organisation_obj = organisation  # get organisation from requested user

    def __enter__(self):
        # Entry Setup
        set_current_tenant(
            self.organisation_obj
        )  # setting current tenant for requested user

    def __exit__(self, type, value, traceback):
        # Exit Setup
        # here can write exit condition
        set_current_tenant(None)




def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class RegisterUser(APIView):
    # authentication_classes = [IsAuthenticated]
    def post(self, request,*args, **kwargs):
        post_data = request.data
        email = post_data.get("email")
        password = post_data.get("password")
        username=post_data.get("username")

        if not email or not password or not username: 
            return Response({"error": "Email, username and password are required"}, status=status.HTTP_400_BAD_REQUEST)
        
        user,created = models.User.objects.get_or_create(username =username, email=email)
        if not created:
            return Response({"error": "username is taken try with another one"}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(password)
        user.save()

        token = get_tokens_for_user(user)

        return Response({"success": "user created",
                         "token": token}, status=status.HTTP_201_CREATED)
    


class UserTokens(APIView):
    def post(self, request, *args, **kwargs):
        post_data = request.data
        username = post_data.get("username")
        password = post_data.get("password")
        if not username or not password:
            return Response({"error": "username and password are required"}, status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(username=username, password=password)
        if user is None:
            return Response({"error": "Invalid username or password"}, status=status.HTTP_400_BAD_REQUEST)
        
        token = get_tokens_for_user(user)
        return Response({"success": "user logged in",
                         "token": token}, status=status.HTTP_200_OK)


class AllCollegesAPI(APIView):
    permission_classes = [IsAuthenticated]
    def initial(self, request, *args, **kwargs):
        return super().initial(request, *args, **kwargs)
    

    def get(self, request, *args, **kwargs):
        
        all_college_data = models.College.objects.all().values("id",'name', )
        return Response(data={"all_college_data":all_college_data},
        status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        post_data = request.data

class CollegeAPI(APIView):
    permission_classes = [IsAuthenticated]
    def initial(self, request, *args, **kwargs):
        self.college_id  = kwargs["college_id"]
        return super().initial(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        clg_obj = models.College.objects.first()
        print("current tenant is :",get_current_tenant())
        tenant_data = models.Student.objects.all().values("id",'user__username','college__name', 'college_id')
        return Response(data=tenant_data,status=status.HTTP_200_OK)

