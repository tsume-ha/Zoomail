import datetime
import json
from django.core.exceptions import ObjectDoesNotExist

from django.test import TestCase, Client

from .models import Cashe


def make_user(self, year=2019):
    self.user = User.objects.create_user(email=str(year) + "mail@gmail.com", year=year)
    self.user.last_name = "京大"
    self.user.first_name = "太郎"
    self.user.furigana = "きょうだいたろう"
    self.user.save()
    return self.user


def login(self, user):
    self.client = Client()
    self.client.force_login(user)
    return user


def logout(self):
    self.client = Client()
    self.client.logout()


class probideAPITest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        # Crate test Data
        today = datetime.date.today()
        bulk = []
        for i in range(10):
            tmp = Cashe(
                date=today + datetime.timedelta(days=i),
                room="Room_" + str(i),
                updated_at=datetime.datetime.now(),
                event_id=str(i),
            )
            bulk.append(tmp)
        Cashe.objects.bulk_create(bulk)

    def test_today_API(self):
        logout(self)
        response = self.client.get("/api/meeting_room/today/")
        self.assertEqual(response.status_code, 200)
        content = json.loads(response.content)
        casheContent = Cashe.objects.get(date=datetime.date.today())
        self.assertEqual(content["date"], casheContent.date.strftime("%Y-%m-%d"))
        self.assertEqual(content["room"], casheContent.room)

    def test_get31day_API(self):
        logout(self)
        response = self.client.get("/api/meeting_room/get31day/")
        self.assertEqual(response.status_code, 200)
        content = json.loads(response.content)
        for i in range(len(content["rooms"])):
            date = datetime.date.today() + datetime.timedelta(days=i)
            try:
                casheContent = Cashe.objects.get(date=date)
                self.assertEqual(content["rooms"][i]["date"], date.strftime("%Y-%m-%d"))
                self.assertEqual(content["rooms"][i]["room"], casheContent.room)
            except ObjectDoesNotExist:
                self.assertEqual(content["rooms"][i]["date"], date.strftime("%Y-%m-%d"))
                self.assertEqual(content["rooms"][i]["room"], None)
