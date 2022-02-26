from django.db import models
from django.utils import timezone

from members.models import User


class Room(models.Model):
    date = models.DateField(unique=True)
    room_name = models.CharField(max_length=200, null=True, blank=True)
    description = models.CharField(max_length=200, null=True, blank=True)
    updated_at = models.DateTimeField(default=timezone.now)
    updated_by = models.ForeignKey(to=User, null=True, on_delete=models.SET_NULL, related_name="meeting_room_update")

    def __str__(self):
        return self.date.strftime("%Y-%m-%d") + ": " + str(self.room_name)
