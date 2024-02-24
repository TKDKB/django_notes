
from django.contrib.auth import get_user_model
from rest_framework import serializers
from notes.models import Note, Tag


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["id", "username", "email"]


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name"]
        read_only_fields = ["id"]


class NoteSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Note
        fields = ["uuid", "title", "content", "created_at", "image", "mod_time", "user", "is_private", "tags"]
        read_only_fields = ["uuid", "created_at", "mod_time", "user"]


class NotesListSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    tags = TagSerializer(many=True)

    class Meta:
        model = Note
        fields = ["uuid", "title", "created_at", "image", "mod_time", "user", "is_private", "tags"]


class NoteCreateSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    tags = TagSerializer(many=True)

    class Meta:
        model = Note
        fields = ["title", "content", "image", "is_private", "tags"]


class NoteDetailedSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    tags = TagSerializer(many=True)

    class Meta:
        model = Note
        fields = ["uuid", "title", "content", "created_at", "image", "mod_time", "user", "is_private", "tags"]
