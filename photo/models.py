from django.db import models
from members.models import User
from private_storage.fields import PrivateFileField
import datetime
import os


def custom_upload_to(instance, filename):
    held_at = instance.held_at
    path = "photo_album_thumbnail/" + held_at.strftime("%Y_%m_%d")
    extension = os.path.splitext(filename)[-1]
    return path + extension


class PhotoAlbum(models.Model):

    class Meta:
        verbose_name = "アルバム"
        verbose_name_plural = "アルバム"

    title = models.CharField(max_length=200, verbose_name="イベント名")
    url = models.URLField(blank=True, verbose_name="アルバムのURL")
    held_at = models.DateField(verbose_name="イベントを行った日")
    thumbnail = PrivateFileField(
        null=True,
        blank=True,
        verbose_name="サムネイル",
        upload_to=custom_upload_to,
        help_text="JPEGファイルのみ対応しています。<br>5kB以上のファイルをアップロードすると自動的に縮小されます。",
        content_types=["image/jpeg"],
    )
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User, null=True, on_delete=models.SET_NULL, related_name="created_album"
    )

    def __str__(self):
        return self.held_at.strftime("%Y-%m-%d") + " : " + self.title
