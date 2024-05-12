from django.shortcuts import HttpResponse
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from base import models
from django_multitenant.utils import set_current_tenant,get_current_tenant
from rest_framework.permissions import IsAuthenticated


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

class AllCollegesAPI(APIView):
    def initial(self, request, *args, **kwargs):
        return super().initial(request, *args, **kwargs)
    

    def get(self, request, *args, **kwargs):
        
        all_college_data = models.College.objects.all().values("id",'name', )
        return Response(data={"all_college_data":all_college_data},
        status=status.HTTP_200_OK)


        

class CollegeAPI(APIView):
    def initial(self, request, *args, **kwargs):
        self.college_id  = kwargs["college_id"]
        return super().initial(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        clg_obj = models.College.objects.first()
        print("current tenant is :",get_current_tenant())
        tenant_data = models.Student.objects.all().values("id",'user__username','college__name', 'college_id')
        return Response(data=tenant_data,status=status.HTTP_200_OK)

