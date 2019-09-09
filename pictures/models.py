from django.db import models
from members.models import User

class Album(models.Model):
    title = models.CharField(max_length=200, verbose_name='イベント名')
    detail = models.CharField(max_length=200, blank=True, verbose_name='説明（あれば）')
    url = models.URLField(blank=True, verbose_name='アルバムのURL')
    held_at = models.DateField(verbose_name='イベントを行った日')
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='album_creater')
    def __str__(self):
        return self.held_at.strftime('%Y-%m-%d') + ' : ' + self.title
