from django.db import models
from private_storage.fields import PrivateFileField
from members.models import User
import uuid
import os
from django.conf import settings
from PIL import Image
from pdf2image import convert_from_path


def others_custom_upload_to(instance, filename):
    ext = os.path.splitext(filename)[-1]
    return "others/{}{}".format(uuid.uuid4().hex, ext)


def others_custom_thumbnail_upload_to(instance, filename):
    return "others/{}_thumb.jpg".format(uuid.uuid4().hex)


class File(models.Model):
    upload_user = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.SET_NULL
    )
    title = models.CharField(max_length=255, blank=True)
    original_name = models.CharField(max_length=255)
    file = PrivateFileField(upload_to=others_custom_upload_to)
    thumbnail = PrivateFileField(
        upload_to=others_custom_thumbnail_upload_to, blank=True, null=True
    )
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
            thumbnail_path = (
                settings.PRIVATE_STORAGE_ROOT
                / "/others/"
                / os.path.splitext(os.path.basename(self.file.name))[0]
                / "_thumb.jpg"
            )
            img.save(thumbnail_path)
            self.thumbnail = thumbnail_path
            self.save(update_fields=["thumbnail"])

    def create_pdf_thumbnail(self):
        images = convert_from_path(self.file.path, first_page=0, last_page=1)
        if images:
            thumbnail_path = (
                settings.PRIVATE_STORAGE_ROOT
                / "/others/"
                / os.path.splitext(os.path.basename(self.file.name))[0]
                / "_thumb.jpg"
            )
            images[0].save(thumbnail_path, "JPEG")
            self.thumbnail = thumbnail_path
            self.save(update_fields=["thumbnail"])
