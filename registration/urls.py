from django.contrib.auth import views
from django.urls import path
from registration.views import register

urlpatterns = [
    path("register/", register, name="register")]

