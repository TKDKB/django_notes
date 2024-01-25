import datetime

from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from django.core.handlers.wsgi import WSGIRequest
from django.db.models import Q
from .models import User
from django.urls import reverse


def register_empty_fields(request: WSGIRequest):
    if not request.POST.get("username") or not request.POST.get("email") or not request.POST.get("password1"):
        return True
    return False


def register_user_existence(request: WSGIRequest):
    if User.objects.filter(
            Q(username=request.POST["username"]) | Q(email=request.POST["email"])
    ).count() > 0:
        return True

    return False


def register_password_coincidence(request: WSGIRequest):
    if request.POST.get("password1") != request.POST.get("password2"):
        return True

    return False


def register_checker(request: WSGIRequest):
    if register_empty_fields(request):
        return render(request,
                      "registration/register.html",
                      {"errors": "Fill all the fields"}
                      )

    elif register_user_existence(request):
        return render(
            request,
            "registration/register.html",
            {"errors": "User with such username or email already exists"}
        )

    elif register_password_coincidence(request):
        return render(
            request,
            "registration/register.html",
            {"errors": "Passwords are not the same"}
        )
    else:
        return False


def register(request: WSGIRequest):
    if request.method != "POST":
        return render(request, "registration/register.html")
    print("lalala")
    if not register_checker(request):
        User.objects.create_user(
            username=request.POST["username"],
            email=request.POST["email"],
            password=request.POST["password1"]
        )
        return HttpResponseRedirect(reverse('home'))
    return register_checker(request)




# def register1(request: WSGIRequest):
#     if request.method != "POST":
#         return render(request, "registration/register.html")
#
#     if not request.POST.get("username") or not request.POST.get("email") or not request.POST.get("password1"):
#         return render(
#             request,
#             "registration/register.html",
#             {"errors": "Fill all the fields"}
#         )
#
#     # Если уже есть такой пользователь с username или email.
#     if User.objects.filter(
#             Q(username=request.POST["username"]) | Q(email=request.POST["email"])
#     ).count() > 0:
#         return render(
#             request,
#             "registration/register.html",
#             {"errors": "User with such username or email already exists"}
#         )
#
#     # Сравниваем два пароля!
#     if request.POST.get("password1") != request.POST.get("password2"):
#         return render(
#             request,
#             "registration/register.html",
#             {"errors": "Passwords are not the same"}
#         )
#
#     # Создадим учетную запись пользователя.
#     # Пароль надо хранить в БД в шифрованном виде.
#     User.objects.create_user(
#         username=request.POST["username"],
#         email=request.POST["email"],
#         password=request.POST["password1"]
#     )
#     return HttpResponseRedirect(reverse('home'))
