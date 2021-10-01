from django.db import models
from members.models import User
from private_storage.fields import PrivateFileField
import datetime
import os

def custom_upload_to(instance, filename):
    now = datetime.datetime.now()
    path = 'album_thumbnail/' + str(now.year) + '/' + now.strftime('%Y_%m_%d__%H_%M_%S')
    extension = os.path.splitext(filename)[-1]
    return path + extension


class Album(models.Model):
    title = models.CharField(max_length=200, verbose_name='イベント名')
    url = models.URLField(blank=True, verbose_name='アルバムのURL')
    held_at = models.DateField(verbose_name='イベントを行った日')
    thumbnail = PrivateFileField(
        null=True,
        blank=True,
        verbose_name='サムネイル',
        upload_to=custom_upload_to,
        help_text='5kB以上のファイルをアップロードすると自動的に縮小されます。',
        content_types=['image/jpeg', 'image/png'])
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='created_album')
    def __str__(self):
        return self.held_at.strftime('%Y-%m-%d') + ' : ' + self.title
