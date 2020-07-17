from django.test import TestCase, Client
from django.db.models import Count
from django.core.files.uploadedfile import SimpleUploadedFile
from members.models import User
from django.contrib.auth.models import Permission
import os
import json
from .models import Performance, Song
from django.conf import settings


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
    self.performance = Performance.objects.create(
        live_name = 'Test Rehasal 1',
        updated_by = User.objects.get(email=str(user_year) + 'mail@gmail.com')
        )
    mp3dir = os.path.join(settings.BASE_DIR, 'player', 'test.mp3')
    with open(mp3dir, 'rb') as file:
        Song.objects.create(
            performance = self.performance,
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


class PlayerViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Make_User(cls)
        Make_Song(cls)
        cls.performance_num = Performance.objects.aggregate(Count('pk'))['pk__count']

    def test_player_index_logOUT(self):
        User_LogOUT(self)
        response = self.client.get('/player/')
        self.assertEqual(response.status_code, 302)
        url_redial_to = response.url
        response = self.client.get(url_redial_to)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin/login.html')

    def test_player_index_logIN(self):
        Force_Login(self)
        response = self.client.get('/player/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<title>リハ音源')
        self.assertContains(response, 'TestSong')

    def test_player_playlist_logOUT(self):
        User_LogOUT(self)
        for index in range(self.performance_num+3):
            pk = index + 1
            response = self.client.get('/player/playlist/' + str(pk))
            self.assertEqual(response.status_code, 302)
            url_redial_to = response.url
            response = self.client.get(url_redial_to)
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, 'admin/login.html')

    def test_player_playlist_logIN(self):
        Force_Login(self)
        for index in range(self.performance_num+3):
            pk = index + 1
            response = self.client.get('/player/playlist/' + str(pk))
            if index < self.performance_num:
                self.assertEqual(response.status_code, 200)
                # self.assertContains(response, 'TestSong')
                # self.songs_in_playlist = Song.objects.filter(performance=Performance.objects.get(pk=pk))
                # for song in self.songs_in_playlist:
                #     self.assertContains(response, song.file.url)
            else:
                self.assertEqual(response.status_code, 404)

    def test_player_upload_logOUT(self):
        User_LogOUT(self)
        response = self.client.get('/player/upload/')
        self.assertEqual(response.status_code, 302)
        url_redial_to = response.url
        response = self.client.get(url_redial_to)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin/login.html')

    def test_player_index_logIN(self):
        Force_Login(self)
        response = self.client.get('/player/upload/')
        self.assertEqual(response.status_code, 403)

    def test_player_songdata_logOUT(self):
        User_LogOUT(self)
        for index in range(self.performance_num+3):
            pk = index + 1
            response = self.client.get('/player/api/live/' + str(pk))
            self.assertEqual(response.status_code, 302)
            url_redial_to = response.url
            response = self.client.get(url_redial_to)
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, 'admin/login.html')

    def test_player_songdata_logIN(self):
        Force_Login(self)
        for index in range(self.performance_num+3):
            pk = index + 1
            response = self.client.get('/player/api/live/' + str(pk))
            if index < self.performance_num:
                self.assertEqual(response.status_code, 200)
            else:
                self.assertEqual(response.status_code, 404)


class uploadTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Make_User(cls, year=2019)
        Make_User(cls, year=2018)

    def test_player_upload_logOUT(self):
        User_LogOUT(self)
        response = self.client.get('/player/upload/')
        self.assertEqual(response.status_code, 302)
        url_redial_to = response.url
        response = self.client.get(url_redial_to)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin/login.html')

    def test_player_upload_logIN_withOUT_permission(self):
        Force_Login(self, 2019)
        response = self.client.get('/player/upload/')
        self.assertEqual(response.status_code, 403)

    def test_player_upload_logIN_with_permission(self):
        Get_a_Permission(self, 2019)
        Force_Login(self, 2019)
        response = self.client.get('/player/upload/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'player/upload.html')

        mp3dir = os.path.join(settings.BASE_DIR, 'player', 'test.mp3')
        with open(mp3dir, 'rb') as file:
            data = {
                'track_num': 1,
                'song_name': 'test_song',
                'livename': 'test_live',
                'recorded_at': '2020-07-01',
                'file': file,
            }
            request = self.client.post('/player/upload/', data)
            self.assertEqual(request.status_code, 200)
            response = self.client.get('/player/')
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, 'player/index.html')
            self.assertContains(response, data['livename'])
            self.assertContains(response, data['song_name'])

            uploaded_song = Song.objects.get(song_name=data['song_name'])
            performance = Performance.objects.get(live_name=data['livename'])
            response = self.client.get(
                '/player/api/live/{}'.format(performance.pk)
                )
            self.assertEqual(response.status_code, 200)

            self.assertContains(response, data['livename'])
            self.assertContains(response, data['song_name'])
            

    def test_player_upload_logIN_withOUT_permission(self):
        User_LogOUT(self)
        Force_Login(self, 2018)
        response = self.client.get('/player/upload/')
        self.assertEqual(response.status_code, 403)

        mp3dir = os.path.join(settings.BASE_DIR, 'player', 'test.mp3')
        with open(mp3dir, 'rb') as file:
            data = {
                'track_num': 1,
                'song_name': 'test_song',
                'livename': 'test_live',
                'recorded_at': '2020-07-01',
                'file': file,
            }
            request = self.client.post('/player/upload/', data)
            self.assertEqual(request.status_code, 403)
            response = self.client.get('/player/')
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, 'player/index.html')
            self.assertNotContains(response, data['livename'])
            self.assertNotContains(response, data['song_name'])



