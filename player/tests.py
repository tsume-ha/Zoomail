from django.test import TestCase, Client
from django.db.models import Count
from django.core.files.uploadedfile import SimpleUploadedFile
from members.models import User
from django.contrib.auth.models import Group
import os
from .models import Performance, Song
from django.conf import settings


def User_LogOUT(self):
    self.client = Client()
    self.client.logout()

def Make_User(self,year=2019):
    self.user = User.objects.create_user(email=str(year) + 'mail@gmail.com', year=year)

def User_LogIN(self,year=2019):
    return self.client.force_login(User.objects.get(email=str(year) + 'mail@gmail.com'))

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

def Make_Group(self):
    return Group.objects.create(name='RecordingGroup')

def User_LogIN_and_Add_a_Group(self, year=2019):
    user = User.objects.get(email=str(year) + 'mail@gmail.com')
    admin_group = Group.objects.get(name='RecordingGroup')
    admin_group.user_set.add(user)
    self.client.force_login(user)
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
            self.assertTemplateUsed(response, 'admin/login.html')

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
        self.assertTemplateUsed(response, 'admin/login.html')


    def test_player_index_logIN(self):
        User_LogIN(self)
        response = self.client.get('/player/songupload/')
        self.assertEqual(response.status_code, 403)

class SongUploadTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Make_User(cls, year=2019)
        Make_User(cls, year=2018)
        Make_Group(cls)

    def test_player_upload_logOUT(self):
        User_LogOUT(self)
        response = self.client.get('/player/songupload/')
        self.assertEqual(response.status_code, 302)
        url_redial_to = response.url
        response = self.client.get(url_redial_to)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin/login.html')

    def test_player_upload_logIN_withOUT_permission(self):
        User_LogIN(self, 2019)
        response = self.client.get('/player/songupload/')
        self.assertEqual(response.status_code, 403)

    def test_player_upload_logIN_with_permission(self):
        User_LogIN_and_Add_a_Group(self, 2019)
        response = self.client.get('/player/songupload/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'player/songupload.html')

        mp3dir = os.path.join(settings.BASE_DIR, 'player', 'test.mp3')
        data = {}
        with open(mp3dir, 'rb') as file:
            data = {
                'livename': 'テストライブ',
                'recorded_at': '2019-01-01',
                'form-0-song_name': 'テスト曲１',
                'form-0-song_file': SimpleUploadedFile("test.mp3", file.read())
            }
        request = self.client.post('/player/songupload/', data)
        self.assertEqual(request.status_code, 302)
        url_redial_to = request.url
        response = self.client.get(url_redial_to)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'player/playlist.html')
        self.assertContains(response, data['livename'])
        self.assertContains(response, data['form-0-song_name'])
        
        User_LogOUT(self)
        User_LogIN(self, 2018)
        response = self.client.get('/player/songupload/')
        self.assertEqual(response.status_code, 403)
        response = self.client.get(url_redial_to)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'player/playlist.html')
        self.assertContains(response, data['livename'])
        self.assertContains(response, data['form-0-song_name'])

class SongUploadTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Make_User(cls, year=2019)
        Make_User(cls, year=2018)
        Make_Group(cls)
        Make_Song(cls, user_year=2019)
        cls.performance = Performance.objects.get(live_name='Test Rehasal 1')

    def test_player_edit_logOUT(self):
        User_LogOUT(self)
        response = self.client.get('/player/edit/' + str(self.performance.pk))
        self.assertEqual(response.status_code, 302)
        url_redial_to = response.url
        response = self.client.get(url_redial_to)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin/login.html')

    def test_player_edit_logIN_withOUT_permission(self):
        User_LogIN(self, 2019)
        response = self.client.get('/player/edit/' + str(self.performance.pk))
        self.assertEqual(response.status_code, 403)

    def test_player_upload_logIN_with_permission(self):
        User_LogIN_and_Add_a_Group(self, 2019)
        response = self.client.get('/player/edit/' + str(self.performance.pk))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'player/edit.html')
        
        self.song = Song.objects.get(song_name='TestSong')
        mp3dir = os.path.join(settings.BASE_DIR, 'player', 'test.mp3')
        data = {}
        with open(mp3dir, 'rb') as file:
            data = {
                'form-0-track_num': 1,
                'form-0-song_name': self.song.song_name + '_changed',
                'form-0-id': self.song.id,
                'form-1-file': SimpleUploadedFile("test.mp3", file.read()),
                'form-1-track_num': '',
                'form-1-song_name': '',
                'form-1-file': '',
                'form-1-id': '',
                'form-2-track_num': '',
                'form-2-song_name': '',
                'form-2-file': '',
                'form-2-id': '',
                'form-3-track_num': '',
                'form-3-song_name': '',
                'form-3-file': '',
                'form-3-id': '',
                'form-TOTAL_FORMS': ['4'],
                'form-INITIAL_FORMS': ['1'],
                'form-MIN_NUM_FORMS': ['0'],
                'form-MAX_NUM_FORMS': ['1000'],
            }
        request = self.client.post('/player/edit/' + str(self.performance.pk), data)
        self.assertEqual(request.status_code, 302)
        url_redial_to = request.url
        response = self.client.get(url_redial_to)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'player/playlist.html')
        self.assertContains(response, self.performance.live_name)
        self.assertContains(response, data['form-0-song_name'])
        
        User_LogOUT(self)
        User_LogIN(self, 2018)
        response = self.client.get('/player/songupload/')
        self.assertEqual(response.status_code, 403)
        response = self.client.get(url_redial_to)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'player/playlist.html')
        self.assertContains(response, self.performance.live_name)
        self.assertContains(response, data['form-0-song_name'])