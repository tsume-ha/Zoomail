import datetime
from django.db import models

from django.conf import settings
from . import service

class Cashe(models.Model):
    date = models.DateField()
    room = models.CharField(
        max_length=200
    )

class Room:
    # def __init__(self):
        # self.dc = datastore_client.createDatastore()

    # def getByDate(self, date):
    #     key = self.dc.key("datecache", date.strftime('%Y-%m-%d'))
    #     if self.dc.get(key) == None:
    #         return self.getByDateAPI(date)

    #     return self.dc.get(key)['room']

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
        print(events_result)
        # self.__dateCache(date, events[0]['summary'])
        return events[0]['summary']

    # def getByRangeAPI(self, start, end):
    #     start = start.replace(hour=0, minute=0, second=0, microsecond=0)
    #     end = (end + datetime.timedelta(days=1)).replace(hour=0,
    #                                                      minute=0, second=0, microsecond=0)
    #     calendarService = service.createService()
    #     events_result = calendarService.events().list(
    #         calendarId='meeting-room@ku-unplugged.net',
    #         timeMin=start.isoformat() + 'Z',
    #         timeMax=end.isoformat() + 'Z',
    #         maxResults=(end - start).days + 1,
    #         singleEvents=True,
    #         orderBy='startTime'
    #     ).execute()
    #     events = events_result.get('items', [])

    #     roomList = {}

    #     # キーの順番を確保(python 3.7 から保存される)するため, 先にキーを入れておく
    #     date = start.replace()
    #     while(date < end):
    #         roomList[date.strftime('%Y-%m-%d')] = ''
    #         date = date + datetime.timedelta(days=1)

    #     while(True):
    #         for event in events:
    #             eventStart = datetime.datetime.strptime(
    #                 event['start'].get('date'), '%Y-%m-%d')
    #             eventEnd = datetime.datetime.strptime(
    #                 event['end'].get('date'), '%Y-%m-%d')
    #             targetDate = eventStart.replace()
    #             while targetDate < eventEnd:
    #                 if start <= targetDate and targetDate < end:
    #                     roomList[targetDate.strftime(
    #                         '%Y-%m-%d')] = event['summary']

    #                 targetDate = targetDate + datetime.timedelta(days=1)

    #         pageToken = events_result.get('nextPageToken')
    #         if pageToken == None:
    #             break

    #         events_result = calendarService.events().list(
    #             calendarId='meeting-room@ku-unplugged.net',
    #             maxResults=1,
    #             singleEvents=True,
    #             orderBy='startTime',
    #             pageToken=pageToken
    #         ).execute()
    #         events = events_result.get('items', [])

    #     return roomList

    # def next31days(self):
    #     key = self.dc.key(
    #         "monthcache", datetime.datetime.now().strftime('%Y-%m-%d'))
    #     if self.dc.get(key) == None:
    #         return self.next31daysAPI()

    #     return self.dc.get(key)['room']

    # def next31daysAPI(self):
    #     start = datetime.datetime.now()
    #     end = datetime.datetime.now() + datetime.timedelta(days=35)
    #     rooms = self.getByRangeAPI(start, end)
    #     date = end.replace()
    #     while(True):
    #         if rooms[date.strftime('%Y-%m-%d')] == "":
    #             del rooms[date.strftime('%Y-%m-%d')]
    #         else:
    #             break

    #         date = date - datetime.timedelta(days=1)

    #     return self.__monthCache(start, rooms)

    # def __dateCache(self, date, room):
    #     key = self.dc.key("datecache", date.strftime('%Y-%m-%d'))
    #     entity = datastore.Entity(key)
    #     entity['room'] = room
    #     self.dc.put(entity)

    # def __monthCache(self, date, rooms):
    #     key = self.dc.key("monthcache", date.strftime('%Y-%m-%d'))
    #     entity = datastore.Entity(key)
    #     # cloud datastore は, dictionary の順序が保持されないため配列で保存
    #     roomArray = []
    #     for date, room in rooms.items():
    #         roomArray.append({'date': date, 'room': room})

    #     entity['room'] = roomArray
    #     return roomArray
