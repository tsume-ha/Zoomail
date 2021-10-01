import os

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from imagekit import ImageSpec
from imagekit.processors import ResizeToFill

from .models import Album

class Thumbnail(ImageSpec):
    processors = [ResizeToFill(400, 300)]
    format = 'JPEG'
    options = {'quality': 60}


@receiver(post_save, sender=Album)
def diminish_thumbnail(sender, instance, *args, **kwargs):
    if instance.thumbnail.size > 50*1000:# 50kB
        source_file = open(instance.thumbnail.path, 'rb')
        image_generator = Thumbnail(source=source_file)
        result = image_generator.generate()
        dest = open(instance.thumbnail.path, 'wb')
        dest.write(result.read())
        dest.close()


@receiver(post_delete, sender=Album)
def delete_thumbnail(sender, instance, *args, **kwargs):
    if instance.thumbnail and os.path.isfile(instance.thumbnail.path):
        os.remove(instance.thumbnail.path)
