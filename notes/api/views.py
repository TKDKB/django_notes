import json
import uuid
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, ListCreateAPIView
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.serializers import ModelSerializer
from notes.models import Note, Tag
from .permissions import IsOwner, NotPrivateOrDontShow
from .serializers import NotesListSerializer, NoteCreateSerializer, NoteDetailedSerializer, NoteSerializer, TagSerializer
from rest_framework.filters import SearchFilter, OrderingFilter


class TagsListTagCreateAPIView(ListCreateAPIView):
    queryset = Tag.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [SearchFilter]
    search_fields = ["@name"]
    serializer_class = TagSerializer


class NotesListNoteCreateAPIView(ListCreateAPIView):
    queryset = Note.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly, NotPrivateOrDontShow]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["@title", "@content"]
    ordering_fields = ["mod_time"]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return NoteSerializer
        return NotesListSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class REDNoteAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    lookup_field = "uuid"
    lookup_url_kwarg = "uuid"
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwner, NotPrivateOrDontShow]


class GenericNotesListAPIView(GenericAPIView):

    queryset = Note.objects.all()

    # def get_queryset(self):
    #     return self.queryset

    def get_serializer_class(self):
        if self.request.method == "POST":
            return NoteCreateSerializer
        return NotesListSerializer

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data
        return Response(data)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        note = serializer.save(user=self.request.user)

        serializer = NoteDetailedSerializer(instance=note)
        return Response(serializer.data, status=201)


class GenericREDNoteAPIView(GenericAPIView):
    queryset = Note.objects.all()

    def get_serializer_class(self):
        if self.request.method == "GET":
            return NoteDetailedSerializer
        return NoteCreateSerializer

    def get(self, request, uuid, *args, **kwargs):
        note = get_object_or_404(self.get_queryset(), uuid=uuid)
        serializer = self.get_serializer(instance=note)
        return Response(serializer.data)

    def put(self, request, uuid, *args, **kwargs):
        note = get_object_or_404(self.get_queryset(), uuid=uuid)
        serializer = self.get_serializer(data=request.data, instance=note)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def patch(self, request, uuid, *args, **kwargs):
        note = get_object_or_404(self.get_queryset(), uuid=uuid)
        serializer = self.get_serializer(data=request.data, instance=note, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, uuid, *args, **kwargs):
        note = get_object_or_404(self.get_queryset(), uuid=uuid)
        note.delete()
        return Response(status=204)