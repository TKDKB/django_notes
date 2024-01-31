import datetime
from django.db.models.signals import post_delete, pre_save
from django.conf import settings
from django.dispatch import receiver
import uuid
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser


# class User(AbstractUser):
#     phone = models.CharField(max_length=11, null=True, blank=True)


def upload_to(instance: "Note", filename: str) -> str:
    return f"{instance.uuid}/{filename}"


class Note(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to=upload_to, null=True)
    mod_time = models.DateTimeField(null=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    is_private = models.BooleanField(default=False)
    objects = models.Manager()

    def save(self, *args, **kwargs):
        try:
            this = Note.objects.get(id=self.id)
            if this.image != self.image:
                this.image.delete()
        except:
            pass
        super(Note, self).save(*args, **kwargs)

    class Meta:
        ordering = ['-created_at']


@receiver(post_delete, sender=Note)
def delete_note(sender, instance: Note, **kwargs):
    if instance.image:
        note_media_folder = (settings.MEDIA_ROOT / str(instance.uuid))
        for file in note_media_folder.glob("*"):
            instance.image.delete(False)
            file.unlink(missing_ok=True)
        note_media_folder.rmdir()


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



