import os

from django.db import models
from django.utils import timezone

from private_storage.fields import PrivateFileField

from members.models import User


class Content(models.Model):
    title = models.CharField(max_length=50, verbose_name='タイトル')
    file = PrivateFileField(
        upload_to='others/',
        max_file_size=30*1024*1024,
        verbose_name='ファイル'
    )
    detail = models.CharField(max_length=200, null=True, blank=True, verbose_name='詳細事項')
    created_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='others_create')
    updated_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='others_update')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    index = models.IntegerField(
        default=0,
        blank=True,
        help_text='ページ内での表示順です。初期値は「0」で、大きいほど上に、小さいほど(負の整数も可)下に表示されます。'
    )

    def __str__(self):
        return self.title

    def extension(self):
        _, extension = os.path.splitext(self.file.name)
        return extension
