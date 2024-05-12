from django.urls import path
from base import api

urlpatterns = [
    path("home", api.AllCollegesAPI.as_view(), name='home'),
    path('<college_id>/college', api.CollegeAPI.as_view(), name='college'),
]