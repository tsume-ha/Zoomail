from django.test import TestCase, Client, RequestFactory
from django.db.models import Count
from django.core.files.uploadedfile import SimpleUploadedFile
from members.models import User
import datetime
import os
from .models import Performance, Song
from config.settings import BASE_DIR


def User_LogOUT(self):
    self.client = Client()
    self.client.logout()

def Make_User(self,year=2019):
    self.user = User.objects.create_user(email=str(year) + 'mail@gmail.com', year=year) #changed from google_account

def User_LogIN(self,year=2019):
    self.client.force_login(User.objects.get(email=str(year) + 'mail@gmail.com')) #changed from google_account

def Make_Song(self, user_year=2019):
    self.performance = Performance.objects.create(
        live_name = 'Test Rehasal 1',
        updated_by = User.objects.get(email=str(user_year) + 'mail@gmail.com') #changed from google_account
        )
    mp3dir = os.path.join(BASE_DIR, 'player', 'test.mp3')
    with open(mp3dir, 'rb') as file:
        Song.objects.create(
            performance = self.performance,
            track_num = 1,
            song_name = 'TestSong',
            file = SimpleUploadedFile("test.mp3", file.read()),
            updated_by = User.objects.get(email=str(user_year) + 'mail@gmail.com') #changed from google_account
            )




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
        # self.assertContains(response, 'Google account')

    def test_player_index_logIN(self):
        User_LogIN(self)
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
            # self.assertContains(response, 'Google account')

    def test_player_playlist_logIN(self):
        User_LogIN(self)
        for index in range(self.performance_num+3):
            pk = index + 1
            response = self.client.get('/player/playlist/' + str(pk))
            if index < self.performance_num:
                self.assertEqual(response.status_code, 200)
                self.assertContains(response, 'TestSong')
                self.songs_in_playlist = Song.objects.filter(performance=Performance.objects.get(pk=pk))
                for song in self.songs_in_playlist:
                    self.assertContains(response, song.file.url)
            else:
                self.assertEqual(response.status_code, 404)

    def test_player_songupload_logOUT(self):
        User_LogOUT(self)
        response = self.client.get('/player/songupload/')
        self.assertEqual(response.status_code, 302)
        url_redial_to = response.url
        response = self.client.get(url_redial_to)
        self.assertEqual(response.status_code, 200)
        # self.assertContains(response, 'Google account')


    def test_player_index_logIN(self):
        User_LogIN(self)
        response = self.client.get('/player/songupload/')
        self.assertEqual(response.status_code, 403)