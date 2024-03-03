import datetime
import os
from django_last_hope.settings import MEDIA_ROOT
from django.db.models.signals import post_delete, pre_save
from django.conf import settings
from django.dispatch import receiver
import uuid
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from ckeditor.fields import RichTextField


# class User(AbstractUser):
#     phone = models.CharField(max_length=11, null=True, blank=True)


def upload_to(instance: "Note", filename: str) -> str:
    return f"{instance.uuid}/{filename}"


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Note(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    content = RichTextField()
    created_at = models.DateTimeField(auto_now_add=True)
    # image = models.ImageField(upload_to="images/", null=True, blank=True)
    image = models.CharField(max_length=255, null=True, blank=True)

    mod_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    is_private = models.BooleanField(default=False)
    tags = models.ManyToManyField(Tag, related_name="notes", null=True, blank=True)
    objects = models.Manager()

    def save(self, *args, **kwargs):
        try:
            this = Note.objects.get(uuid=self.uuid)
            if self.image and this.image and this.image != self.image:
                print("bitch")
                os.remove(MEDIA_ROOT / "images" / this.image)
                (MEDIA_ROOT / "images" / this.image).unlink(missing_ok=True)
        except:
            pass
        super(Note, self).save(*args, **kwargs)

    class Meta:
        ordering = ['mod_time']
        indexes = [
            models.Index(fields=("mod_time",), name="mod_time_index"),
            # models.Index(fields=("title",), name="title_index"),
        ]

    def __str__(self):
        return f"Заметка: \"{self.title}\""


@receiver(post_delete, sender=Note)
def delete_note(sender, instance: Note, **kwargs):
    if instance.image:
        # note_media_folder = (settings.MEDIA_ROOT / "images")
        os.remove(MEDIA_ROOT / "images" / instance.image)
        (MEDIA_ROOT / "images" / instance.image).unlink(missing_ok=True)
        # note_media_folder.rmdir()


# @receiver(pre_save, sender=Note)
# def edit_note(sender, instance: Note, **kwargs):
#     if instance.image:
#         note_media_folder = (settings.MEDIA_ROOT / str(instance.uuid))
#         for file in note_media_folder.glob("*"):
#             #if str(file) != str(instance.image):  # Сравнение путей до файлов
#             file.unlink(missing_ok=True)

# @receiver(signal=models.signals.post_init, sender=Note)
# def post_init_handler(instance, **kwargs):
#     if instance.image:
#         instance.original_image = instance.image
#
#
# @receiver(signal=models.signals.post_save, sender=Note)
# def post_save_handler(instance, **kwargs):
#     if instance.image:
#         note_media_folder = (settings.MEDIA_ROOT / str(instance.uuid))
#         if not instance.image == instance.original_image:
#             for file in note_media_folder.glob("*"):
#                 if str(file) == str(instance.original_image):
#                     file.unlink(missing_ok=True)
#                 instance.original_image = instance.image



