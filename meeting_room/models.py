import datetime
import json
from googleapiclient.errors import HttpError
from django.db import models
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist

from django.conf import settings
from . import service

class Cashe(models.Model):
    date = models.DateField(unique=True)
    room = models.CharField(max_length=200)
    updated_at = models.DateTimeField(default=timezone.now)
    event_id = models.CharField(max_length=255)

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
        print(events)
        return events[0]['summary']

    def createByDateAPI(self, date, room):
        event = {
            'summary': room,
            'start': {
                'date': date.strftime('%Y-%m-%d'),
                'timeZone': 'Asia/Tokyo',
            },
            'end': {
                'date': date.strftime('%Y-%m-%d'),
                'timeZone': 'Asia/Tokyo',
            },
        }
        calendarService = service.createService()
        events_result = calendarService.events().insert(
            calendarId=settings.GOOGLE_CALENDAR_ID,
            body=event
            ).execute()
        return events_result

    def createByDate(self, date, room):
        if type(date) is not list:
            date = [date,]
        for d in date:
            result = self.createByDateAPI(
                date=d, room=room)
            object = Cashe.objects.create(
                date=d,
                room=room,
                event_id=result['id']
            )

    def deleteByDateAPI(self, date):
        """ 
        dateで受け渡された日付のデータを削除します
        """
        cashe = Cashe.objects.get(date=date)
        calendarService = service.createService()
        calendarService.events().delete(
            calendarId=settings.GOOGLE_CALENDAR_ID,
            eventId=cashe.event_id
            ).execute()
        
    def deleteByDate(self, *date):
        for d in date:
            try:
                cashe = Cashe.objects.get(date=d)
                self.deleteByDateAPI(date=d)
                cashe.delete()
            except ObjectDoesNotExist:
                # Casheが無かったらこのままおわり
                continue
            except HttpError as e:
                reason = json.loads(e.content).get('error').get('errors')[0].get('message')
                # if e.resp.status == 410:
                if reason == 'Resource has been deleted':
                    # Casheは残り、Calendarは削除済み
                    cashe.delete()
                    continue
                # 他のエラーがあったら追加する
                print(reason)

