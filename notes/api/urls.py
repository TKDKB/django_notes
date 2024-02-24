from django.urls import path
from registration.views import register
from . import views
from .views import NotesListNoteCreateAPIView, REDNoteAPIView, TagsListTagCreateAPIView

app_name = "api"

urlpatterns = [
    path("notes/", NotesListNoteCreateAPIView.as_view(), name="notes-list"),
    path("notes/<uuid>", REDNoteAPIView.as_view(), name="note"),
    path("tags/", TagsListTagCreateAPIView.as_view(), name="tags-list"),
]

