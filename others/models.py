from django.db import models
from private_storage.fields import PrivateFileField
from members.models import User
import uuid
import os
from io import BytesIO
from django.core.files.base import ContentFile
from PIL import Image
from pdf2image import convert_from_path


def others_custom_upload_to(instance, filename):
    ext = os.path.splitext(filename)[-1]
    return "others/{}{}".format(uuid.uuid4().hex, ext)


def others_custom_thumbnail_upload_to(instance, filename):
    return "others/{}_thumb.jpg".format(uuid.uuid4().hex)


class File(models.Model):
    filename = models.CharField(max_length=255, blank=True, null=False)
    file = PrivateFileField(upload_to=others_custom_upload_to)
    thumbnail = PrivateFileField(
        upload_to=others_custom_thumbnail_upload_to, blank=True, null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="created_other_file",
    )
    updated_by = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="updated_other_file",
    )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.file and self.thumbnail is None:
            self.generate_thumbnail()

    def generate_thumbnail(self):
        if self.file.name.lower().endswith((".jpg", ".jpeg", ".png", ".gif")):
            self.create_image_thumbnail()
        elif self.file.name.lower().endswith(".pdf"):
            self.create_pdf_thumbnail()

    def create_image_thumbnail(self):
        with Image.open(self.file.path) as img:
            img.thumbnail((100, 100))
            thumb_io = BytesIO()
            img.save(thumb_io, format="JPEG")
            thumb_content = ContentFile(thumb_io.getvalue())
            self.thumbnail.save(
                os.path.splitext(os.path.basename(self.file.name))[0] + "_thumb.jpg",
                thumb_content,
            )

    def create_pdf_thumbnail(self):
        images = convert_from_path(self.file.path, first_page=0, last_page=1)
        if images:
            thumb_io = BytesIO()
            images[0].save(thumb_io, format="JPEG")
            thumb_content = ContentFile(thumb_io.getvalue())
            self.thumbnail.save(
                os.path.splitext(os.path.basename(self.file.name))[0] + "_thumb.jpg",
                thumb_content,
            )
