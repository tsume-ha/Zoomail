import os
import json

from django.test import TestCase, Client
from django.db.models import Count
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import Permission

from django.conf import settings
from .models import Live, Song
from members.models import User


def User_LogOUT(self):
    self.client = Client()
    self.client.logout()

def Make_User(self,year=2019):
    user = User.objects.create_user(
        email=str(year) + 'mail@gmail.com',
        year=year
    )
    user.first_name = str(year) + '名前'
    user.last_name = str(year) + '名字'
    user.furigana = 'ふりがな'
    user.receive_email = str(year) + 'mail@gmail.com'
    user.save()
    return user

def Force_Login(self,year=2019):
    user = User.objects.get(email=str(year) + 'mail@gmail.com')
    self.client = Client()
    self.client.force_login(user)
    return user

def Make_Song(self, user_year=2019):
    self.live = Live.objects.create(
        live_name = 'Test Rehasal 1',
        updated_by = User.objects.get(email=str(user_year) + 'mail@gmail.com')
        )
    mp3dir = os.path.join(settings.BASE_DIR, 'sound', 'test.mp3')
    with open(mp3dir, 'rb') as file:
        Song.objects.create(
            live = self.live,
            track_num = 1,
            song_name = 'TestSong',
            file = SimpleUploadedFile("test.mp3", file.read()),
            updated_by = User.objects.get(email=str(user_year) + 'mail@gmail.com')
            )

def Get_a_Permission(self, year=2019):
    user = User.objects.get(email=str(year) + 'mail@gmail.com')
    permission = Permission.objects.get(codename="add_song")
    user.user_permissions.add(permission)
    return user


class SoundViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Make_User(cls)
        Make_Song(cls)
        cls.live_num = Live.objects.aggregate(Count('pk'))['pk__count']

    def test_sound_index_logOUT(self):
        User_LogOUT(self)
        response = self.client.get('/sound/')
        self.assertEqual(response.status_code, 302)
        url_redial_to = response.url
        response = self.client.get(url_redial_to)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin/login.html')

    def test_sound_index_logIN(self):
        Force_Login(self)
        response = self.client.get('/sound/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<title>リハ音源')
        self.assertContains(response, 'TestSong')

    def test_sound_playlist_logOUT(self):
        User_LogOUT(self)
        for index in range(self.live_num+3):
            pk = index + 1
            response = self.client.get('/sound/' + str(pk) + '/')
            self.assertEqual(response.status_code, 302)
            url_redial_to = response.url
            response = self.client.get(url_redial_to)
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, 'admin/login.html')

    def test_sound_playlist_logIN(self):
        Force_Login(self)
        for index in range(self.live_num+3):
            pk = index + 1
            response = self.client.get('/sound/' + str(pk) + '/')
            if index < self.live_num:
                self.assertEqual(response.status_code, 200)
            else:
                self.assertEqual(response.status_code, 404)

    def test_sound_upload_logOUT(self):
        User_LogOUT(self)
        response = self.client.get('/sound/upload/')
        self.assertEqual(response.status_code, 302)
        url_redial_to = response.url
        response = self.client.get(url_redial_to)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin/login.html')

    def test_sound_index_logIN(self):
        Force_Login(self)
        response = self.client.get('/sound/upload/')
        self.assertEqual(response.status_code, 403)

    def test_sound_songdata_logOUT(self):
        User_LogOUT(self)
        for index in range(self.live_num+3):
            pk = index + 1
            response = self.client.get('/sound/' + str(pk) + '/json/')
            self.assertEqual(response.status_code, 302)
            url_redial_to = response.url
            response = self.client.get(url_redial_to)
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, 'admin/login.html')

    def test_sound_songdata_logIN(self):
        Force_Login(self)
        for index in range(self.live_num+3):
            pk = index + 1
            response = self.client.get('/sound/' + str(pk) + '/json/')
            if index < self.live_num:
                self.assertEqual(response.status_code, 200)
            else:
                self.assertEqual(response.status_code, 404)


class uploadTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Make_User(cls, year=2019)
        Make_User(cls, year=2018)

    def test_sound_upload_logOUT(self):
        User_LogOUT(self)
        response = self.client.get('/sound/upload/')
        self.assertEqual(response.status_code, 302)
        url_redial_to = response.url
        response = self.client.get(url_redial_to)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin/login.html')

    def test_sound_upload_logIN_withOUT_permission(self):
        Force_Login(self, 2019)
        response = self.client.get('/sound/upload/')
        self.assertEqual(response.status_code, 403)

    def test_sound_upload_logIN_with_permission(self):
        Get_a_Permission(self, 2019)
        Force_Login(self, 2019)
        response = self.client.get('/sound/upload/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sound/upload.html')

        mp3dir = os.path.join(settings.BASE_DIR, 'sound', 'test.mp3')
        with open(mp3dir, 'rb') as file:
            data = {
                'track_num': 1,
                'song_name': 'test_song',
                'livename': 'test_live',
                'recorded_at': '2020-07-01',
                'file': file,
            }
            request = self.client.post('/sound/upload/', data)
            self.assertEqual(request.status_code, 200)
            response = self.client.get('/sound/')
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, 'sound/index.html')
            self.assertContains(response, data['livename'])
            self.assertContains(response, data['song_name'])

            live = Live.objects.get(live_name=data['livename'])
            response = self.client.get(
                '/sound/' + str(live.pk) + '/json/'
                )
            self.assertEqual(response.status_code, 200)

            self.assertContains(response, data['livename'])
            self.assertContains(response, data['song_name'])
            
    def test_sound_upload_logIN_withOUT_permission(self):
        User_LogOUT(self)
        Force_Login(self, 2018)
        response = self.client.get('/sound/upload/')
        self.assertEqual(response.status_code, 403)

        mp3dir = os.path.join(settings.BASE_DIR, 'sound', 'test.mp3')
        with open(mp3dir, 'rb') as file:
            data = {
                'track_num': 1,
                'song_name': 'test_song',
                'livename': 'test_live',
                'recorded_at': '2020-07-01',
                'file': file,
            }
            request = self.client.post('/sound/upload/', data)
            self.assertEqual(request.status_code, 403)
            response = self.client.get('/sound/')
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, 'sound/index.html')
            self.assertNotContains(response, data['livename'])
            self.assertNotContains(response, data['song_name'])



