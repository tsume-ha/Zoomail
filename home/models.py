from django.db import models
from django.utils import timezone


class Announcement(models.Model):
    text = models.TextField(blank=False, null=False)
    created_at = models.DateTimeField(
        blank=False, null=False,
        default=timezone.now)
    def __str__(self):
        return self.created_at.strftime('%Y_%m_%d') + ' ' + self.text

class NewContent(models.Model):
    index = models.PositiveSmallIntegerField(unique=True)
    genre = models.CharField(max_length=30, null=False)
    title = models.CharField(max_length=30, null=False)
    path = models.CharField(max_length=60, null=False)
    date = models.DateTimeField()

    def __str__(self) -> str:
        return '{} - {} - {}'.format(self.index, self.genre, self.title)
