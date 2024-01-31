import datetime

from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from django.core.handlers.wsgi import WSGIRequest
from django.db.models import Q
from .models import Note
from registration.models import User
from django.urls import reverse
# Create your views here.


def home_page_view(request: WSGIRequest):
    notes = Note.objects.all()
    context: dict = {
        "notes": notes
    }
    return render(request, "home.html", context)


def filter_notes_view(request: WSGIRequest):
    search = request.GET.get("search", "")

    print("def filter notes view | search", search)

    if search:
        notes_queryset = Note.objects.filter(Q(title__icontains=search) | Q(content__icontains=search))
    else:
        notes_queryset = Note.objects.all()


    print(notes_queryset.query)
    context: dict = {
        "notes": notes_queryset,
        "search_value_note": search,
    }
    return render(request, "home.html", context)


def greetings_page_view(request: WSGIRequest):
    return render(request, "greeting.html")


def delete_note_view(request: WSGIRequest, note_uuid: int):
    Note.objects.filter(uuid=note_uuid).delete()
    return HttpResponseRedirect(reverse('home'))


def edit_note_view(request: WSGIRequest, note_uuid: int):
    note = Note.objects.get(uuid=note_uuid)
    if request.method == "GET":
        return render(request, "edit_note.html", {"note": note})
    elif request.method == "POST" and "confirm" in request.POST:
        print(request.FILES)
        images = request.FILES.getlist("notenewImage")
        note.title = request.POST["title"]
        note.content = request.POST["content"]
        note.mod_time = datetime.datetime.now()
        if images:
            note.image = images[0]
        note.save()
        return HttpResponseRedirect(reverse('show-note', args=[note_uuid]))


def create_note_view(request: WSGIRequest):

    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    if request.method == "POST":
        if "create" in request.POST:
            print(request.FILES)
            images = request.FILES.getlist("noteImage")
            note = Note.objects.create(
                title=request.POST["title"],
                content=request.POST["content"],
                user=request.user,
                image=images[0] if images else None,
            )
            if 'switch' in request.POST:
                flex_switch_value = request.POST['switch']
                print("switch value:", flex_switch_value)
                if flex_switch_value == 'on':
                    note.is_private = True
                    note.save()
                else:
                    note.is_private = False
                    note.save()
            return HttpResponseRedirect(reverse('show-note', args=[note.uuid]))
        else:
            return HttpResponseRedirect(reverse('home'))
    return render(request, "new_note.html")


def about_us_page_view(request):
    return render(request, 'about_us.html')


def show_note_view(request: WSGIRequest, note_uuid: int):
    if request.method == "POST" and "delete" in request.POST:
        # Note.objects.filter(uuid=note_uuid).delete()
        # return HttpResponseRedirect(reverse('home'))
        return delete_note_view(request, note_uuid)
    else:
        try:
            note = Note.objects.get(uuid=note_uuid)  # Получение только ОДНОЙ записи.

        except Note.DoesNotExist:
            # Если не найдено такой записи.
            raise Http404

        return render(request, "note.html", {"note": note})


# def register(request: WSGIRequest):
#     if request.method != "POST":
#         return render(request, "registration/register.html")
#     print(request.POST)
#     if not request.POST.get("username") or not request.POST.get("email") or not request.POST.get("password1"):
#         return render(
#             request,
#             "registration/register.html",
#             {"errors": "Fill all the fields"}
#         )
#     print(User.objects.filter(
#             Q(username=request.POST["username"]) | Q(email=request.POST["email"])
#     ))
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


def author_notes_view(request: WSGIRequest, username: str):
    notes_queryset = Note.objects.filter(user__username=username)
    context: dict = {
        "notes": notes_queryset,
        "author": username
    }
    return render(request, "author_notes.html", context)
