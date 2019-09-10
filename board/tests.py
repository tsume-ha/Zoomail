from django.test import TestCase, Client
from django.db.models import Count
from members.models import User
import os
import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Message, MessageYear, Attachment
from .forms import validation_error_messages
from config.settings import BASE_DIR

# >> py manage.py test board.tests.AuthentificationSendTest
# でclassごとにテストできる


# HTTP CODE
    # 200 success
    # 302 redial
    # 403 forbidden
    # 404 not found
    # 500 server error


def User_LogOUT(self):
    self.client = Client()
    self.client.logout()

def Make_User_and_LogIN(self,year=2019):
    self.user = User.objects.create_user(email=str(year) + 'mail@gmail.com', year=year) # changed from google_account
    self.client = Client()
    self.client.force_login(self.user)

def User_LogIN(self,year=2019):
    self.client.force_login(User.objects.get(email=str(year) + 'mail@gmail.com')) # changed from google_account

def CreateMessage(self, year, is_attachment=False):
    nowtime = datetime.datetime.now()
    user = User.objects.get(email=str(year) + 'mail@gmail.com') # changed from google_account
    for messageyear in [0,year]: # 全回と回生の２件を作る
        content_data = Message(
            title='Title Example ' + str(messageyear),
            content='Content Example \n'*10,
            attachment=is_attachment,
            sender=user,
            writer=user,
            created_at=nowtime,
            updated_at=nowtime
        )
        content_data.save()
        content_data.years.create(year=messageyear)
        if is_attachment:
            file = request.FILES["select_file"]
            content_data.attachments.create(attachment_file=file)
        content_data.save()

def CreateMessages(self, TestYears):
    for User_Year in TestYears:
        Make_User_and_LogIN(self,year=User_Year)
        CreateMessage(self, year=User_Year)
        User_LogOUT(self)


class AuthentificationReadViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.TestYears = list(range(2015,2020))
        CreateMessages(cls, cls.TestYears)
        cls.MessageCount = Message.objects.aggregate(Count('pk'))['pk__count']
        # => 5学年*2通 = 合計10通


    def test_read_index_logOUT(self):
        User_LogOUT(self)
        response = self.client.get('/read/')
        self.assertEqual(response.status_code, 302)
        url_redial_to = response.url
        response = self.client.get(url_redial_to)
        self.assertEqual(response.status_code, 200)
        # self.assertContains(response, 'Google account')

    def test_read_index_logIN(self):
        User_LogIN(self)
        response = self.client.get('/read/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'board/index.html')

    def test_read_index_lonIN_with_content(self):
       for User_Year in self.TestYears:
            User_LogIN(self,year=User_Year)
            response = self.client.get('/read/')
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, 'Title Example ' + str(User_Year)) # 同回の回生メーリスは見れているか
            self.assertContains(response, 'Title Example ' + str(0)) # 全回メーリスは見れているか
            self.assertContains(response, 'Content Example') # 詳細まで見れているか

            # 同回以外の学年を抽出
            for DeniedYear in [y for y in self.TestYears if y != User_Year]:
                self.assertNotContains(response, 'Title Example ' + str(DeniedYear)) # 違う学年の回生メーリスが見れていないか

    def test_read_content_logOUT(self):
        User_LogOUT(self)
        for index in range(self.MessageCount+3):
            pk = index + 1
            target = '/read/content/' + str(pk)
            response = self.client.get(target)
            self.assertEqual(response.status_code, 302)
            url_redial_to = response.url
            response = self.client.get(url_redial_to)
            self.assertEqual(response.status_code, 200)
            # self.assertContains(response, 'Google account')

    def test_read_content_logIN(self):
        for User_Year in self.TestYears:
            User_LogIN(self,year=User_Year)
            for index in range(self.MessageCount+3):
                pk = index + 1
                target = '/read/content/' + str(pk)
                response = self.client.get(target)
                if index < self.MessageCount:
                    Message_Year = MessageYear.objects.get(message=Message.objects.get(pk=pk)).year
                    if Message_Year == 0 or Message_Year == User_Year:
                        self.assertEqual(response.status_code, 200)
                    else:
                        self.assertEqual(response.status_code, 302)
                else:
                    self.assertEqual(response.status_code, 404)


class AuthentificationSendTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Make_User_and_LogIN(cls)

    def test_send_view_logOUT(self):
        User_LogOUT(self)
        response = self.client.get('/send/')
        self.assertEqual(response.status_code, 302)
        url_redial_to = response.url
        response = self.client.get(url_redial_to)
        self.assertEqual(response.status_code, 200)
        # self.assertContains(response, 'Google account')

    def test_send_POST_logOUT(self):
        data = {
            'title': 'LogOUT POST test',
            'to': 0,
            'content': 'LogOUT POST test message',
        }
        User_LogOUT(self)
        request = self.client.post('/send/', data)
        self.assertEqual(request.status_code, 302)
        url_redial_to = request.url
        response = self.client.get(url_redial_to)
        self.assertEqual(response.status_code, 200)
        # self.assertContains(response, 'Google account')

        try:
            saved_content = Message.objects.get(title=data['title'])
            self.assertTrue(False)
        except ObjectDoesNotExist:
            self.assertTrue(True)
        

    def test_send_POST_logIN(self):
        data = {
            'title': 'LogIN POST test',
            'to': 0,
            'content': 'LogIN POST test message',
        }
        User_LogIN(self)
        request = self.client.post('/send/', data)
        self.assertEqual(request.status_code, 302)
        url_redial_to = request.url
        self.assertEqual(url_redial_to, '../read/')

        response = self.client.get('/read/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, data['title'])
        
        saved_content = Message.objects.get(title=data['title'])
        target = '/read/content/' + str(saved_content.pk)
        response = self.client.get(target)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, data['content'])

    def test_send_POST_logIN_missing_YEAR(self):
        data = {
            'title': 'LogIN POST test missing YEAR',
            'to': 'error',
            'content': 'LogIN POST test message missing YEAR',
        }
        User_LogIN(self)
        request = self.client.post('/send/', data)
        self.assertEqual(request.status_code, 200)
        self.assertTemplateUsed(request, 'board/send.html')
        self.assertContains(request, data['title'])
        self.assertContains(request, validation_error_messages['no_year'])
        try:
            saved_content = Message.objects.get(title=data['title'])
            self.assertTrue(False)
        except ObjectDoesNotExist:
            self.assertTrue(True)

    def test_send_POST_logIN_missing_TITLE(self):
        data = {
            'title': '',
            'to': 'error',
            'content': 'LogIN POST test message missing TITLE',
        }
        User_LogIN(self)
        request = self.client.post('/send/', data)
        self.assertEqual(request.status_code, 200)
        self.assertTemplateUsed(request, 'board/send.html')
        self.assertContains(request, validation_error_messages['no_title'])
        try:
            saved_content = Message.objects.get(title=data['title'])
            self.assertTrue(False)
        except ObjectDoesNotExist:
            self.assertTrue(True)

    def test_send_POST_logIN_missing_CONTENT(self):
        data = {
            'title': 'LogIN POST test missing CONTENT',
            'to': 'error',
            'content': '',
        }
        User_LogIN(self)
        request = self.client.post('/send/', data)
        self.assertEqual(request.status_code, 200)
        self.assertTemplateUsed(request, 'board/send.html')
        self.assertContains(request, validation_error_messages['no_content'])
        try:
            saved_content = Message.objects.get(title=data['title'])
            self.assertTrue(False)
        except ObjectDoesNotExist:
            self.assertTrue(True)

    def test_send_POST_logIN_with_TextFile(self):
        self.testfiles = [['29MB.txt', 29*1024*1024], ['31MB.txt', 31*1024*1024]]
        User_LogIN(self)
        for textfile in self.testfiles:
            filedir = os.path.join(BASE_DIR, 'board', textfile[0])
            with open(filedir, 'rb') as file:
                data = {
                    'title': 'LogIN POST test with' + textfile[0],
                    'to': 0,
                    'content': 'LogIN POST test message',
                    'attachmentfile': SimpleUploadedFile(textfile[0], file.read()),
                }
                request = self.client.post('/send/', data)
                if textfile[1] < 30*1024*1024:
                    self.assertEqual(request.status_code, 302) # => 成功、read/へ転送
                    url_redial_to = request.url
                    self.assertEqual(url_redial_to, '../read/')

                    response = self.client.get('/read/')
                    self.assertEqual(response.status_code, 200)
                    self.assertContains(response, data['title'])
                    
                    saved_content = Message.objects.get(title=data['title'])
                    target = '/read/content/' + str(saved_content.pk)
                    response = self.client.get(target)
                    self.assertEqual(response.status_code, 200)
                    self.assertContains(response, data['content'])
                    self.assertContains(response, textfile[0])

                else:
                    self.assertEqual(request.status_code, 200) # => 失敗、sendにとどまる
                    self.assertTemplateUsed(request, 'board/send.html')
                    self.assertContains(request, data['title'])
                    self.assertContains(request, validation_error_messages['filesize_limit'])
                    try:
                        saved_content = Message.objects.get(title=data['title'])
                        self.assertTrue(False)
                    except ObjectDoesNotExist:
                        self.assertTrue(True)
