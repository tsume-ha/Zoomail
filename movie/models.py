from django.db import models
from members.models import User


class YoutubeURL(models.Model):
    title = models.CharField(max_length=200, verbose_name="イベント名")
    url = models.CharField(max_length=2000, blank=True, verbose_name="Youtubeの再生URL")
    textcontent = models.TextField(max_length=2000, blank=True, verbose_name="テキスト")
    held_at = models.DateField(verbose_name="イベントを行った日")
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name="movie_creater")

    def __str__(self):
        return self.held_at.strftime("%Y-%m-%d") + " : " + self.title
