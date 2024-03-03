import datetime
import uuid

from django_last_hope import settings
from django.shortcuts import render
from django.db.models import F
from django.contrib.auth.decorators import login_required
from django.contrib.postgres.aggregates import ArrayAgg
from django.http import HttpResponseRedirect, Http404
from django.core.handlers.wsgi import WSGIRequest
from django.db.models import Q
from .models import Note, Tag
from registration.models import User
from django.urls import reverse
from django.views import View
from notes.service import create_note, filter_notes, queryset_optimization
from .history_service import HistoryService
from django.shortcuts import get_object_or_404



# Create your views here.


def home_page_view(request: WSGIRequest):
    notes = queryset_optimization(Note.objects.all())[:100]
    context: dict = {
        "notes": notes
    }
    # for note in notes:
    #     print(note["tags_list"])
    return render(request, "home.html", context)


def filter_notes_view(request: WSGIRequest):
    search = request.GET.get("search", "")
    print("def filter notes view | search", search)

    context: dict = {
        "notes": queryset_optimization(filter_notes(search))[:100],
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
    # notes_queryset = queryset_optimization(Note.objects.filter(uuid=note_uuid))
    # tag_flag = 0
    # if notes_queryset[0]["tags_list"]:
    #     tag_flag = 1
    if request.method == "GET":
        return render(request, "edit_note.html", {"note": note})
    elif request.method == "POST" and "confirm" in request.POST:
        print(request.FILES)
        images = request.FILES.getlist("notenewImage")
        note.title = request.POST["title"]
        note.content = request.POST["content"]
        note.mod_time = datetime.datetime.now()
        tags: list = request.POST.get("tags", "").split(",")
        tags = [tag.strip() for tag in tags]
        for tag in tags:
            if tag == "":
                tags.remove(tag)
        tags_objects = []
        for tag in tags:
            tag_obj, created = Tag.objects.get_or_create(name=tag)
            tags_objects.append(tag_obj)

        note.tags.set(tags_objects)
        if images:
            note.image = images[0]
            with open(f"{settings.MEDIA_ROOT}/images/{note.image}", "wb") as image_file:
                image_file.write(note.image.read())
        note.save()
        # context: dict = {
        #     "notes": notes_queryset[:100]
        # }
        # nlist = list(notes_queryset)
        return HttpResponseRedirect(reverse('show-note', args=[note_uuid]))


@login_required
def create_note_view(request: WSGIRequest):
    #
    # if not request.user.is_authenticated:
    #     return HttpResponseRedirect(reverse('login'))
    if request.method == "POST":
        if "create" in request.POST:
            # # print(request.FILES)
            # images = request.FILES.getlist("noteImage")
            # note = Note.objects.create(
            #     title=request.POST["title"],
            #     content=request.POST["content"],
            #     user=request.user,
            #     image=images[0] if images else None,
            # )
            # if 'switch' in request.POST:
            #     flex_switch_value = request.POST['switch']
            #     # print("switch value:", flex_switch_value)
            #     if flex_switch_value == 'on':
            #         note.is_private = True
            #         note.save()
            #     else:
            #         note.is_private = False
            #         note.save()
            note = create_note(request)
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
        # try:
        #     note = Note.objects.get(uuid=note_uuid)  # Получение только ОДНОЙ записи.
        #
        #
        # except Note.DoesNotExist:
        #     # Если не найдено такой записи.
        #     raise Http404
        history_service = HistoryService(request)
        note = get_object_or_404(Note, uuid=note_uuid)
        history_service.add_to_history(note)
        if len(request.session["history"]) > 20:
            history_service.del_from_history()

        # return HttpResponseRedirect(reverse("show-note", args=note_uuid))

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
    notes_queryset = queryset_optimization(Note.objects.filter(user__username=username))
    for i in User.objects.all():
        print(i.username)
    context: dict = {
        "notes": notes_queryset[:100],
        "author": username
    }
    return render(request, "author_notes.html", context)


@login_required
def edit_user(request: WSGIRequest, username: str):

    user = User.objects.get(username=request.user.username)
    user_tag_list = list(set(Tag.objects.filter(notes__user__username=request.user.username).values_list("name", flat=True)))
    if request.method == 'GET':
        context = {
            "user": user,
            "user_tag_list": user_tag_list,
        }
        return render(request, "user_profile.html", context)
    elif request.method == "POST" and "confirm" in request.POST:
        user.last_name = request.POST["last name"]
        user.first_name = request.POST["first name"]
        user.phone = request.POST["phone"]
        user.save()
        return HttpResponseRedirect(reverse('profile', args=[user.username]))
    elif request.method == "POST" and "change password" in request.POST:
        return HttpResponseRedirect(reverse("send-email"))



# class HistoryAddView(View):
#
#     def post(self, request: WSGIRequest, note_uuid: uuid):
#         history_service = HistoryService(request)
#         note = get_object_or_404(Note, uuid=note_uuid)
#
#         if len(request.session["history"]) < 20:
#             history_service.add_to_history(note)
#         else:
#             history_service.del_from_history()
#
#         return HttpResponseRedirect(reverse("show-note", args=note_uuid))


class HistoryShowView(View):

    def get(self, request: WSGIRequest):
        history_service = HistoryService(request)
        queryset = queryset_optimization(Note.objects.filter(uuid__in=history_service.get_history()))
        return render(request, "home.html", {"notes": queryset})
