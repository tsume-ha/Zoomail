import os

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from mutagen.mp3 import MP3

from .models import Song


@receiver(post_save, sender=Song)
def update_songfile_details(sender, instance, *args, **kwargs):
    if instance.length is None:
        try:
            audio = MP3(instance.file.path)
            length = audio.info.length
            if length > 0:
                instance.length = int(length)
            else:
                instance.length = 0
        except:
            instance.length = 0
        finally:
            instance.save()


@receiver(post_delete, sender=Song)
def delete_file(sender, instance, *args, **kwargs):
    if instance.file and os.path.isfile(instance.file.path):
        os.remove(instance.file.path)
