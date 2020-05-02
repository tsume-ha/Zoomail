import os

from django.db.models.signals import post_delete
from django.dispatch import receiver

from .models import Content


@receiver(post_delete, sender=Content)
def delete_file(sender, instance, *args, **kwargs):
    if instance.file and os.path.isfile(instance.file.path):
        try:
            os.remove(instance.file.path)
        except:
            pass
