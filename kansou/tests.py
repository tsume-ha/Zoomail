from django.test import TestCase, Client
from members.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Kansouyoushi
from django.contrib.auth.models import Group
import os
from django.conf import settings
import datetime

livename = Kansouyoushi.livename


def User_LogOUT(self):
    self.client = Client()
    self.client.logout()

def Make_User(self,year=2019):
    self.user = User.objects.create_user(email=str(year) + 'mail@gmail.com', year=year)


def User_LogIN(self,year=2019):
    self.client.force_login(User.objects.get(email=str(year) + 'mail@gmail.com'))

def User_LogIN_and_Add_AdministerGroup(self,year=2019):
    user = User.objects.get(email=str(year) + 'mail@gmail.com')
    admin_group = Group.objects.create(name='Administer')
    admin_group.user_set.add(user)
    self.client.force_login(user)


def Make_KansouPDF(self, user_year=2019, performed_at=datetime.date.today()):
    Kansouyoushi.objects.all().delete()
    pdfdir = os.path.join(settings.BASE_DIR, 'kansou', 'test.pdf')
    for i in range(len(livename)):
        live = livename[i][0]
        filename = performed_at.strftime('%Y_%m_%d') + '_' + live + '.pdf'
        with open(pdfdir, 'rb') as file:
            Kansouyoushi.objects.create(
                live = live,
                detail = '',
                numbering = 1,
                file = SimpleUploadedFile(filename, file.read()),
                performed_at = performed_at,
                created_by = User.objects.get(email=str(user_year) + 'mail@gmail.com')
                )

class KansouyoushiViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Make_User(cls)
        

    def test_kansou_index_logOUT(self):
        User_LogOUT(self)
        response = self.client.get('/kansou/')
        self.assertEqual(response.status_code, 302)
        url_redial_to = response.url
        response = self.client.get(url_redial_to)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin/login.html')

    def test_kansou_index_logIN(self):
        User_LogIN(self)
        Make_KansouPDF(self)
        response = self.client.get('/kansou/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'kansou/index.html')
        for i in range(len(livename)):
            self.assertContains(response, livename[i][1])
            self.assertContains(response, Kansouyoushi.objects.get(live=livename[i][0]).file.url)
        
    def test_kansou_index_logIN_3_31(self):
        User_LogIN(self)
        day = datetime.date(2018, 3, 31)
        Make_KansouPDF(self, performed_at=day)
        response = self.client.get('/kansou/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'kansou/index.html')
        for i in range(len(livename)):
            self.assertContains(response, livename[i][1])
            self.assertContains(response, Kansouyoushi.objects.get(live=livename[i][0]).file.url)
            self.assertContains(response, str(day.year - 1)+'年度')
            self.assertNotContains(response, str(day.year)+'年度')
            self.assertNotContains(response, str(day.year + 1)+'年度')

    def test_kansou_index_logIN_4_1(self):
        User_LogIN(self)
        day = datetime.date(2018, 4, 1)
        Make_KansouPDF(self, performed_at=day)
        response = self.client.get('/kansou/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'kansou/index.html')
        for i in range(len(livename)):
            self.assertContains(response, livename[i][1])
            self.assertContains(response, Kansouyoushi.objects.get(live=livename[i][0]).file.url)
            self.assertNotContains(response, str(day.year - 1)+'年度')
            self.assertContains(response, str(day.year)+'年度')
            self.assertNotContains(response, str(day.year + 1)+'年度')


    def test_kansou_upload_logIN_POST_withOUT_Permission(self):
        User_LogIN(self)
        response = self.client.get('/kansou/upload/')
        self.assertEqual(response.status_code, 302)
        url_redial_to = response.url
        self.assertEqual(url_redial_to, '/kansou/')

        filedir = os.path.join(settings.BASE_DIR, 'kansou', 'test.pdf')
        with open(filedir, 'rb') as file:
            data = {
                'live': livename[0][0],
                'performed_at': datetime.date.today(),
                'file': SimpleUploadedFile('test.pdf', file.read()),
                }
            request = self.client.post('/kansou/upload/', data)
        self.assertEqual(request.status_code, 302)
        url_redial_to = request.url
        self.assertEqual(url_redial_to, '/kansou/')

        response = self.client.get(url_redial_to)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'kansou/index.html')
        self.assertNotContains(response, '登録しました。')
        self.assertNotContains(response, data['performed_at'].strftime('%Y/%m/%d'))


    def test_kansou_upload_logIN_POST_with_Permission(self):
        User_LogIN_and_Add_AdministerGroup(self)
        response = self.client.get('/kansou/upload/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'kansou/upload.html')
        filedir = os.path.join(settings.BASE_DIR, 'kansou', 'test.pdf')
        with open(filedir, 'rb') as file:
            data = {
                'live': livename[0][0],
                'performed_at': datetime.date.today(),
                'file': SimpleUploadedFile('test.pdf', file.read()),
                }
            request = self.client.post('/kansou/upload/', data)
        self.assertEqual(request.status_code, 302)
        url_redial_to = request.url
        self.assertEqual(url_redial_to, '/kansou/')

        response = self.client.get(url_redial_to)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'kansou/index.html')
        self.assertContains(response, '登録しました。')
        self.assertContains(response, data['performed_at'].strftime('%Y/%m/%d'))