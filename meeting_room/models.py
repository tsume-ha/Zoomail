import datetime
from django.db import models
from django.utils import timezone

from django.conf import settings
from . import service

class Cashe(models.Model):
    date = models.DateField()
    room = models.CharField(max_length=200)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.date.strftime('%Y-%m-%d') + ': ' + self.room

class Room:
    def getByDate(self, date):
        cashe = Cashe.objects.filter(date=date)
        if not cashe.exists():
            room = self.getByDateAPI(date)
            content = Cashe(
                date=date,
                room=room,
            )
            content.save()
            return room
        return cashe[0].room

    def getByDateAPI(self, date):
        start = date.replace(hour=0, minute=0, second=0)
        end = date.replace(hour=23, minute=59, second=59)
        calendarService = service.createService()
        events_result = calendarService.events().list(
            calendarId=settings.GOOGLE_CALENDAR_ID,
            timeMin=start.isoformat() + 'Z',
            timeMax=end.isoformat() + 'Z',
            maxResults=1,
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        events = events_result.get('items', [])
        return events[0]['summary']