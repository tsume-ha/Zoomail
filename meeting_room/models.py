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
    room = models.CharField(max_length=200, null=True)
    updated_at = models.DateTimeField(default=timezone.now)
    event_id = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.date.strftime("%Y-%m-%d") + ": " + str(self.room)


class Room:
    def getByDate(self, date):
        cashe = Cashe.objects.filter(date=date)
        if cashe.exists():
            return {
                "date": date.strftime("%Y-%m-%d"),
                "room": cashe[0].room
                # dateはuniqueなので初めの1つだけとる
            }
        else:
            room = self.getByDateAPI(date)
            content = Cashe(
                date=date,
                room=room,
            )
            content.save()
            return {"date": date.strftime("%Y-%m-%d"), "room": room}

    def getByDateAPI(self, date):
        """
        カレンダーに情報がある：summaryでタイトル部分を返す
        （返り値はString型）
        カレンダーに情報がない：Noneを返す
        """
        start = datetime.datetime.combine(date, datetime.time(hour=0, minute=0, second=0))
        end = datetime.datetime.combine(date, datetime.time(hour=23, minute=59, second=59))
        calendarService = service.createService()
        events_result = (
            calendarService.events()
            .list(
                calendarId=settings.GOOGLE_CALENDAR_ID,
                timeMin=start.isoformat() + "Z",
                timeMax=end.isoformat() + "Z",
                maxResults=1,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
        events = events_result.get("items", [])
        # print(events)
        return events[0]["summary"] if events else None
        # カレンダーにも登録されていなかったらNoneを返す

    def getByDateRange(self, start_date, end_date):
        """
        start_date から end_date までの例会教室のデータを
        [{"date": "YYYY-MM-DD", "room": "4共21"}, ...]
        の形で返す
        """
        query = Cashe.objects.filter(date__gte=start_date, date__lte=end_date).order_by("date").values("date", "room")
        date_list = [start_date + datetime.timedelta(days=i) for i in range((end_date - start_date).days + 1)]

        def seikei(query, date):
            result = list(filter(lambda q: q["date"] == date, query))
            # lambdaがTrueのとき：queryがそのまま返る
            if len(result) == 1:
                return result[0]["room"]
            else:
                return self.getByDate(date)["room"]
                # getByDateでもう一度叩く
                # 初めの1回でキャッシュは保存される

        rooms = [
            {
                "date": d.strftime("%Y-%m-%d"),
                # queryで返ってこなかった日にちは未登録として処理
                "room": seikei(query, d),
            }
            for d in date_list
        ]
        return rooms

    def createAPI(self, room, date):
        event = {
            "summary": room,
            "start": {
                "date": date.strftime("%Y-%m-%d"),
                "timeZone": "Asia/Tokyo",
            },
            "end": {
                "date": date.strftime("%Y-%m-%d"),
                "timeZone": "Asia/Tokyo",
            },
        }
        calendarService = service.createService()
        events_result = calendarService.events().insert(calendarId=settings.GOOGLE_CALENDAR_ID, body=event).execute()
        return events_result

    def create(self, room, date):
        """
        Casheに登録されていないことを前提に
        （updateOrCreateで確認する）
        """
        result = self.createAPI(room=room, date=date)
        Cashe.objects.update_or_create(
            date=date,
            defaults={
                "room": room,
                "event_id": result["id"],
            },
        )
        return result

    def deleteByDateAPI(self, date):
        """
        dateで受け渡された日付のデータを削除します
        """
        cashe = Cashe.objects.get(date=date)
        calendarService = service.createService()
        calendarService.events().delete(calendarId=settings.GOOGLE_CALENDAR_ID, eventId=cashe.event_id).execute()

    def deleteByDate(self, date):
        """
        キャッシュとGoogle Calendarの両方とも消す
        キャッシュが先に消えてる場合はGoogle Calendarはさわらない
        """
        try:
            cashe = Cashe.objects.get(date=date)
            self.deleteByDateAPI(date=date)
            cashe.room = None
            cashe.event_id = None
            cashe.save()
        except ObjectDoesNotExist:
            # Casheが無かったらこのままおわり
            pass
        except HttpError as e:
            if e.resp and e.resp.status and e.resp.status == 410:
                # if reason == 'Resource has been deleted':
                # Casheは残り、Calendarは削除済み
                cashe.room = None
                cashe.event_id = None
                cashe.save()
                return

            # 他のエラーがあったらコードを追加する
            print(e)
            reason = json.loads(e.content).get("error").get("errors")[0].get("message")
            print(reason)

    def updateAPI(self, room, date):
        cashe = Cashe.objects.get(date=date)
        event = {
            "summary": room,
            "start": {
                "date": date.strftime("%Y-%m-%d"),
                "timeZone": "Asia/Tokyo",
            },
            "end": {
                "date": date.strftime("%Y-%m-%d"),
                "timeZone": "Asia/Tokyo",
            },
        }
        calendarService = service.createService()
        updated_event = (
            calendarService.events()
            .update(calendarId=settings.GOOGLE_CALENDAR_ID, eventId=cashe.event_id, body=event)
            .execute()
        )
        return updated_event["updated"]

    def update(self, room, date):
        """
        前提：キャッシュが存在する
        存在の保証はupdateOrCreateで確認する
        """
        cashe = Cashe.objects.get(date=date)
        response = self.updateAPI(room, date)
        cashe.room = room
        cashe.save()

    def updateOrCreate(self, room, date):
        """
        room(新規登録データ)が空の時はdeleteを発火する
        Casheを見てcreateかupdateを発火する
        """
        if not room:
            self.deleteByDate(date)
            return {"status": "deleted"}
        cashe = Cashe.objects.filter(date=date).exclude(room=None)
        try:
            if cashe.exists():
                self.update(room=room, date=date)
                return {"status": "updated"}
            else:
                self.create(room=room, date=date)
                return {"status": "created"}
        except HttpError as e:
            print(e)
            print(e.content)
            reason = "http error"
            reason = json.loads(e.content).get("error").get("errors")[0].get("message")
            if e.resp.status == 410:
                print(reason)

            # これまでに確認したエラーたち
            # 404  update  Casheにあるevent_idがGoogleに存在しない
            # 410  delete  Calendarで削除済みのeventにevent_idからアクセス

            return {"status": "http error", "message": reason, "status_code": e.resp.status}

    def syncFromCalendarToCashe(self):
        """
        Google Calendarからデータを取得しキャッシュに保存させる
        キャッシュは全て上書きする
        """
        now = datetime.datetime.now()
        start = now.replace(hour=0, minute=0, second=0) - datetime.timedelta(days=10)
        end = now.replace(hour=23, minute=59, second=59) + datetime.timedelta(days=50)
        calendarService = service.createService()
        events_result = (
            calendarService.events()
            .list(
                calendarId=settings.GOOGLE_CALENDAR_ID,
                timeMin=start.isoformat() + "Z",
                timeMax=end.isoformat() + "Z",
                singleEvents=True,
                maxResults=70,
                orderBy="startTime",
            )
            .execute()
        )
        events = events_result.get("items", [])

        # 余分なキャッシュを削除する
        event_id_list = [e["id"] for e in events]
        update_query = []
        for query in Cashe.objects.filter(date__gte=start, date__lte=end):
            if query.event_id not in event_id_list and query.room is not None:
                query.room = None
                update_query.append(query)
        Cashe.objects.bulk_update(update_query, fields=["room"])

        # 不足しているキャッシュを追加する
        for e in events:
            if "start" in e and "date" in e["start"]:
                # 終日の予定だけ読み込む
                # print(e['start']['date'], e['summary'])
                s_dt = datetime.datetime.strptime(e["start"]["date"], "%Y-%m-%d")
                start_date = datetime.date(s_dt.year, s_dt.month, s_dt.day)
                e_dt = datetime.datetime.strptime(e["end"]["date"], "%Y-%m-%d")
                end_date = datetime.date(e_dt.year, e_dt.month, e_dt.day)
                if start_date == end_date:
                    Cashe.objects.update_or_create(
                        date=start_date, defaults={"room": e["summary"], "event_id": e["id"]}
                    )
                else:
                    """
                    連続した日にちがあるときは
                    一旦これを消して、1日ごとに作り直す
                    """
                    event_id = e["id"]
                    calendarService.events().delete(calendarId=settings.GOOGLE_CALENDAR_ID, eventId=event_id).execute()
                    Cashe.objects.filter(event_id=event_id).delete()
                    datelist = [start_date + datetime.timedelta(days=i) for i in range((end_date - start_date).days)]
                    self.updateOrCreate(e["summary"], *datelist)
