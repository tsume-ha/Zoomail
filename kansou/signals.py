import os

from django.db.models.signals import post_delete
from django.dispatch import receiver

from .models import Kansouyoushi

@receiver(post_delete, sender=Kansouyoushi)
def delete_file(sender, instance, *args, **kwargs):
    if instance.file and os.path.isfile(instance.file.path):
        os.remove(instance.file.path)
