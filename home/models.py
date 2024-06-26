from django.db import models
from django.utils import timezone


def ContentLog(LIST_NUM=3):
    from django.urls import reverse
    from kansou.models import Kansouyoushi
    from movie.models import YoutubeURL
    from pictures.models import Album
    from sound.models import Live

    kansou_list = [
        ("kansou", "感想用紙", q.created_at, q.title, reverse("kansou:index"))
        for q in Kansouyoushi.objects.order_by("-created_at")[:LIST_NUM]
    ]
    movie_list = [
        ("movie", "ライブ映像", q.created_at, q.title, reverse("movie:index"))
        for q in YoutubeURL.objects.order_by("-created_at")[:LIST_NUM]
    ]
    pictures_list = [
        ("pictures", "写真", q.created_at, q.title, reverse("pictures:index"))
        for q in Album.objects.order_by("-created_at")[:LIST_NUM]
    ]
    sound_list = [
        ("sound", "リハ音源", q.updated_at, q.live_name, reverse("sound:playlist", args=[q.pk]))
        for q in Live.objects.order_by("-updated_at")[:LIST_NUM]
    ]

    log_list = kansou_list + movie_list + pictures_list + sound_list
    log_list.sort(key=lambda tup: tup[2], reverse=True)

    return log_list[:LIST_NUM]


class Announcement(models.Model):
    text = models.TextField(blank=False, null=False)
    created_at = models.DateTimeField(blank=False, null=False, default=timezone.now)

    def __str__(self):
        return self.created_at.strftime("%Y_%m_%d") + " " + self.text


class NewContent(models.Model):
    index = models.PositiveSmallIntegerField(unique=True)
    genre = models.CharField(max_length=30, null=False)
    title = models.CharField(max_length=30, null=False)
    path = models.CharField(max_length=60, null=False)
    date = models.DateTimeField()

    def __str__(self) -> str:
        return "{} - {} - {}".format(self.index, self.genre, self.title)
