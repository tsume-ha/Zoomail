from django.test import TestCase, Client
from members.models import User
from django.contrib.auth.models import Permission
from django.core.exceptions import ObjectDoesNotExist
from .models import Album
import datetime


def User_LogOUT(self):
    self.client = Client()
    self.client.logout()


def Make_User(self, year=2019):
    self.user = User.objects.create_user(email=str(year) + "mail@gmail.com", year=year)
    self.user.last_name = "京大"
    self.user.first_name = "太郎"
    self.user.furigana = "きょうだいたろう"
    self.user.save()
    return self.user


def User_LogIN_and_Get_a_Permission(self, groupname, year=2019):
    user = User.objects.get(email=str(year) + "mail@gmail.com")
    permission = Permission.objects.get(codename="add_album")
    user.user_permissions.add(permission)
    self.client.force_login(user)
    return user


def User_LogIN(self, year=2019):
    self.user = User.objects.get(email=str(year) + "mail@gmail.com")
    self.client.force_login(self.user)
    return self.user


class PicturesViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Make_User(cls)

    def test_pictures_index_logOUT(self):
        User_LogOUT(self)
        response = self.client.get("/pictures/")
        self.assertEqual(response.status_code, 302)
        url_redial_to = response.url
        response = self.client.get(url_redial_to)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "admin/login.html")

    def test_pictures_index_logIN(self):
        User_LogIN(self)
        response = self.client.get("/pictures/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pictures/index.html")


class PicturesTestwithModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        Make_User(cls)

    def test_pictures_index_with_records_logIN(self):
        user = User_LogIN(self)
        record_dates = ["2019-03-30", "2019-04-01"]
        for date in record_dates:
            Album.objects.create(title="album" + date[5], url="http://example.com", held_at=date, created_by=user)
        response = self.client.get("/pictures/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pictures/index.html")
        for date in record_dates:
            self.assertContains(response, "album" + date[5])

    def test_pictures_Register_POST_LogOUT(self):
        data = {
            "title": "n月ライブ",
            "held_at": "2019-04-01",
            "url": "https://example.com",
        }
        User_LogOUT(self)
        request = self.client.post("/pictures/register/", data)
        self.assertEqual(request.status_code, 302)
        url_redial_to = request.url
        response = self.client.get(url_redial_to)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "admin/login.html")

        try:
            saved_content = User.objects.get(last_name=data["title"])
            self.assertTrue(False)
        except ObjectDoesNotExist:
            self.assertTrue(True)

    def test_pictures_Register_POST_No_AUTH_LogIN(self):
        data = {
            "title": "n月ライブ",
            "held_at": "2019-04-01",
            "url": "https://example.com",
        }
        User_LogIN(self)
        request = self.client.post("/pictures/register/", data)
        self.assertEqual(request.status_code, 302)
        url_redial_to = request.url
        response = self.client.get(url_redial_to)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pictures/index.html")

        try:
            saved_content = Album.objects.get(title=data["title"])
            self.assertTrue(False)
        except ObjectDoesNotExist:
            self.assertTrue(True)

    def test_pictures_Register_POST_AUTH_LogIN(self):
        data = {
            "title": "n月ライブ",
            "held_at": "2019-04-01",
            "url": "https://example.com",
        }
        User_LogIN_and_Get_a_Permission(self, "PhotographersGroup")
        request = self.client.post("/pictures/register/", data)
        self.assertEqual(request.status_code, 302)
        url_redial_to = request.url
        response = self.client.get(url_redial_to)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pictures/index.html")

        try:
            saved_content = Album.objects.get(title=data["title"])
            self.assertTrue(True)
        except ObjectDoesNotExist:
            self.assertTrue(False)
        User_LogOUT(self)

        # Other User Login
        other_users_year = list(range(2000, 2010))
        for user_year in other_users_year:
            Make_User(self, year=user_year)
            User_LogIN(self, year=user_year)
            response = self.client.get("/pictures/")
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, "pictures/index.html")
            self.assertContains(response, data["title"])
