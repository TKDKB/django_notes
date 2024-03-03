import datetime

from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.handlers.wsgi import WSGIRequest
from django.db.models import Q
from .models import User
from django.urls import reverse
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from registration.forms import PasswordResetForm
from registration.email_senders import PasswordResetEmailSender


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
            password=request.POST["password1"],
            is_active=True,
        )
        return HttpResponseRedirect(reverse('home'))
    return register_checker(request)


def send_email(request: WSGIRequest):
    # if request.method == "POST":
        PasswordResetEmailSender(request, request.user).send_mail()
        # return HttpResponseRedirect("registration/message.html")
        return render(request, "registration/message.html")

# def change_password_receiver(request: WSGIRequest, token: str, uidb: str):
#     user_id = force_str(urlsafe_base64_decode(uidb))
#     user = get_object_or_404(User, id=user_id)
#     if default_token_generator.check_token(user, token):
#         return HttpResponseRedirect(reverse("actually-change-password"))
#     return render(request, "registration/invalid-password-reset.html")
#
#
# def actually_change_password(request: WSGIRequest, uidb, token):
#     form = PasswordResetForm()
#     if request.method == 'POST':
#         form = PasswordResetForm(request.POST)
#         if form.is_valid():
#             print("lallalal")
#
#             request.user.save(update_fields=["password"])
#             update_session_auth_hash(request, request.user)
#             return HttpResponseRedirect(reverse("login"))
#
#     return render(request, 'registration/password-reset-form.html', {'form': form})


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
def change_password_receiver(request: WSGIRequest, token: str, uidb: str):
    user_id = force_str(urlsafe_base64_decode(uidb))
    user = get_object_or_404(User, id=user_id)
    if default_token_generator.check_token(user, token):
        form = PasswordResetForm()
        if request.method == 'POST':
            form = PasswordResetForm(request.POST)
            if form.is_valid():
                user.set_password(form.cleaned_data["password1"])
                user.save(update_fields=["password"])
                update_session_auth_hash(request, request.user)
                return HttpResponseRedirect(reverse("login"))
        return render(request, 'registration/password-reset-form.html', {'form': form})

    return render(request, "registration/invalid-password-reset.html")
