import datetime
import os

from django.db import models
from django.utils import timezone
from private_storage.fields import PrivateFileField

from members.models import User


def custom_upload_to(instance, filename):
    now = datetime.datetime.now()
    path = 'music/' + now.strftime('%Y/%m/%d/') + \
        now.strftime('%Y_%m_%d__%H_%M_%S')
    extension = os.path.splitext(filename)[-1]
    return path + extension


class Performance(models.Model):
    live_name = models.CharField(max_length=255)
    recorded_at = models.DateField(default=timezone.now)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    updated_by = models.ForeignKey(
        User, null=True, on_delete=models.SET_NULL, related_name='perform_updated_by')

    def __str__(self):
        return str(self.id) + self.live_name


class Song(models.Model):
    performance = models.ForeignKey(Performance, on_delete=models.CASCADE)
    track_num = models.IntegerField()
    song_name = models.CharField(max_length=500)
    file = PrivateFileField(upload_to=custom_upload_to, null=True)
    length = models.IntegerField(null=True, blank=True)  # time(seconds)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    updated_by = models.ForeignKey(
        User, null=True, on_delete=models.SET_NULL, related_name='song_updated_by')

    def __str__(self):
        return str(self.track_num) + ' ' + self.song_name
