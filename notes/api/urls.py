
from django.urls import path, include
import django_last_hope.settings
from registration.views import register
from . import views
from .views import NotesListNoteCreateAPIView, REDNoteAPIView, TagsListTagCreateAPIView, UploadImageAPIView

app_name = "api"

urlpatterns = [
    path("notes/", NotesListNoteCreateAPIView.as_view(), name="notes-list"),
    path("notes/<uuid>", REDNoteAPIView.as_view(), name="note"),
    path("tags/", TagsListTagCreateAPIView.as_view(), name="tags-list"),
    path("image/", UploadImageAPIView.as_view(), name="note-image"),
    path("auth/", include("djoser.urls.authtoken"))
]

