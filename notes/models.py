import datetime
import uuid
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser


# class User(AbstractUser):
#     phone = models.CharField(max_length=11, null=True, blank=True)


class Note(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    mod_time = models.DateTimeField(null=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    is_private = models.BooleanField(default=False)
    objects = models.Manager()

    class Meta:
        ordering = ['-created_at']
