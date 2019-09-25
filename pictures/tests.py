from django.test import TestCase, Client
from members.models import User
from django.contrib.auth.models import Group
from django.core.exceptions import ObjectDoesNotExist
from .models import Album
import datetime

def User_LogOUT(self):
    self.client = Client()
    self.client.logout()

def Make_User(self,year=2019):
    self.user = User.objects.create_user(email=str(year) + 'mail@gmail.com', year=year)
    return self.user

def User_LogIN_and_Add_a_Group(self, groupname, year=2019):
    user = User.objects.get(email=str(year) + 'mail@gmail.com')
    admin_group = Group.objects.create(name=groupname)
    admin_group.user_set.add(user)
    self.client.force_login(user)
    return user

def User_LogIN(self,year=2019):
    self.user = User.objects.get(email=str(year) + 'mail@gmail.com')
    self.client.force_login(self.user)
    return self.user


class PicturesViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Make_User(cls)

    def test_pictures_index_logOUT(self):
        User_LogOUT(self)
        response = self.client.get('/pictures/')
        self.assertEqual(response.status_code, 302)
        url_redial_to = response.url
        response = self.client.get(url_redial_to)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin/login.html')

    def test_pictures_index_logIN(self):
        User_LogIN(self)
        response = self.client.get('/pictures/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pictures/index.html')

    def test_pictures_index_with_records_logIN(self):
        user = User_LogIN(self)
        record_dates = [
            '2019-03-30',
            '2019-04-01'
        ]
        for date in record_dates:
            Album.objects.create(
                title = 'album' +date[5],
                url = 'http://example.com',
                held_at = date,
                created_by = user
                )
        response = self.client.get('/pictures/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pictures/index.html')
        for date in record_dates:
            self.assertContains(response, 'album' +date[5])


