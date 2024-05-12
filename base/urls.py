from django.urls import path
from base import api

urlpatterns = [
    path("home", api.AllCollegesAPI.as_view(), name='home'),
    path("register", api.RegisterUser.as_view(), name='register'),
    path("get-token", api.UserTokens.as_view(), name='get_token'),
    path('<college_id>/college', api.CollegeAPI.as_view(), name='college'),
]