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

    def createAPI(self, room, date):
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

    def create(self, room, date):
        """
        Casheに登録されていないことを前提に
        （updateOrCreateで確認する）
        """
        result = self.createAPI(
            room=room, date=date)
        Cashe.objects.create(
            room=room,
            date=date,
            event_id=result['id']
        )
        return result

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
        """
        キャッシュとGoogle Calendarの両方とも消す
        キャッシュが先に消えてる場合はGoogle Calendarはさわらない
        """
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
                # 他のエラーがあったらコードを追加する
                print(reason)

    def updateAPI(self, room, date):
        cashe = Cashe.objects.get(date=date)
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
        updated_event = calendarService.events().update(
            calendarId=settings.GOOGLE_CALENDAR_ID,
            eventId=cashe.event_id,
            body=event
            ).execute()
        return updated_event['updated']

    def update(self, room, date):
        """
        前提：キャッシュが存在する
        存在の保証はupdateOrCreateで確認する
        """
        cashe = Cashe.objects.get(date=date)
        response = self.updateAPI(room, date)
        cashe.room = room
        cashe.save()

    def updateOrCreate(self, room, *date):
        """
        dateで複数のdatetime.dateを受けることを明示するために
        可変長引数に
        """
        for d in date:
            try:
                cashe = Cashe.objects.get(date=d)
                self.update(room=room, date=d)
            except ObjectDoesNotExist:
                self.create(room=room, date=d)
            except HttpError as e:
                reason = json.loads(e.content).get('error').get('errors')[0].get('message')
                # if e.resp.status == 410:

    # def syncFromCalendarToCashe(self, *date=None):
    #     """
    #     Google Calendarからデータを取得しキャッシュに保存させる
    #     キャッシュは全て上書きする
    #     """
    #     pass