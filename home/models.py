from django.db import models
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from members.models import User

class SpecialPage(models.Model):
    title = models.CharField(max_length=200)
    url = models.CharField(max_length=200)
    key = models.CharField(max_length=64)
    html_name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.title + ' ' + self.html_name


KANSOU = 1
SOUND = 2
MOVIE = 3
ALBUM = 4

MODEL_FLAG_CHOICES = (
    (KANSOU, 'Kansou'),
    (SOUND, 'Sound'),
    (MOVIE, 'Movie'),
    (ALBUM, 'Album'),
)

class ContentLog(models.Model):
    action_time = models.DateTimeField(
        default=timezone.now,
        editable=False,
    )
    content_type = models.ForeignKey(
        ContentType,
        models.SET_NULL,
        blank=True, null=True,
    )