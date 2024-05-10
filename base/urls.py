from django.urls import path
from base import api

urlpatterns = [
    path("", api.Home, name='home'),
]