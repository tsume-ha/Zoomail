from django.db import models
from django.utils import timezone


def content_log(LIST_NUM=3):
    from django.urls import reverse
    from kansou.models import Kansouyoushi
    from movie.models import YoutubeURL
    from photo.models import PhotoAlbum

    kansou_list = [
        ("kansou", "感想用紙", q.created_at, q.title, reverse("kansou:index"))
        for q in Kansouyoushi.objects.order_by("-created_at")[:LIST_NUM]
    ]
    movie_list = [
        ("movie", "ライブ映像", q.created_at, q.title, reverse("movie:index"))
        for q in YoutubeURL.objects.order_by("-created_at")[:LIST_NUM]
    ]
    photo_list = [
        ("photo", "写真", q.created_at, q.title, reverse("photo:index"))
        for q in PhotoAlbum.objects.order_by("-created_at")[:LIST_NUM]
    ]
    log_list = kansou_list + movie_list + photo_list
    log_list.sort(key=lambda tup: tup[2], reverse=True)

    return log_list[:LIST_NUM]


class Announcement(models.Model):
    class Meta:
        verbose_name = "お知らせ"
        verbose_name_plural = "お知らせ"
        ordering = ["-created_at"]

    text = models.TextField(blank=False, null=False)
    created_at = models.DateTimeField(blank=False, null=False, default=timezone.now)

    def __str__(self):
        return self.created_at.strftime("%Y_%m_%d") + " " + self.text
