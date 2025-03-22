from django.db import models
from members.models import User
import uuid
import os
from django.utils.deconstruct import deconstructible
from django.conf import settings
from PIL import Image
from pdf2image import convert_from_path


@deconstructible
class PathAndRename:
    def __init__(self, sub_path):
        self.sub_path = sub_path

    def __call__(self, instance, filename):
        ext = filename.split(".")[-1]
        # set filename as random string
        filename = "{}.{}".format(uuid.uuid4().hex, ext)
        # return the whole path to the file
        return os.path.join(self.sub_path, filename)


class File(models.Model):
    upload_user = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.SET_NULL
    )
    title = models.CharField(max_length=255, blank=True)
    original_name = models.CharField(max_length=255)
    file = models.FileField(upload_to=PathAndRename("uploads/"))
    thumbnail = models.ImageField(upload_to="thumbnails/", blank=True, null=True)
    description = models.TextField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.file:
            self.generate_thumbnail()

    def generate_thumbnail(self):
        if self.file.name.lower().endswith((".jpg", ".jpeg", ".png", ".gif")):
            self.create_image_thumbnail()
        elif self.file.name.lower().endswith(".pdf"):
            self.create_pdf_thumbnail()

    def create_image_thumbnail(self):
        with Image.open(self.file.path) as img:
            img.thumbnail((100, 100))
            thumbnail_path = os.path.join(
                settings.MEDIA_ROOT, "thumbnails", os.path.basename(self.file.name)
            )
            img.save(thumbnail_path)
            self.thumbnail = thumbnail_path
            self.save(update_fields=["thumbnail"])

    def create_pdf_thumbnail(self):
        images = convert_from_path(self.file.path, first_page=0, last_page=1)
        if images:
            thumbnail_path = os.path.join(
                settings.MEDIA_ROOT,
                "thumbnails",
                os.path.basename(self.file.name) + ".jpg",
            )
            images[0].save(thumbnail_path, "JPEG")
            self.thumbnail = thumbnail_path
            self.save(update_fields=["thumbnail"])
