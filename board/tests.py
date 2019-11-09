from django.test import TestCase, Client
from django.db.models import Count
from members.models import User
import os
import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Message, MessageYear
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
    user = User.objects.get(email=str(year) + 'mail@gmail.com')
    self.client.force_login(user)
    return user

def CreateMessage(self, year, is_attachment=False):
    nowtime = datetime.datetime.now()
    user = User.objects.get(email=str(year) + 'mail@gmail.com') # changed from google_account
    for messageyear in [0,year]: # 全回と回生の２件を作る
        content_data = Message(
            title='Title Example ' + str(messageyear),
            content='Content Example \n'*10,
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
        self.assertTemplateUsed(response, 'admin/login.html')

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
            self.assertTemplateUsed(response, 'admin/login.html')

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
        self.assertTemplateUsed(response, 'admin/login.html')

# {
# 'csrfmiddlewaretoken': ['BPe33gaRWSrrfJYJJAN3v0h5De8yxBQIDzigof4dAaJXmpF8vjEpk1qxb67N9Gn4'],
# 'title': ['テストメーリス'],
# 'year_choice': ['2019'],
# 'written_by': ['2019-1'],
# 'to': ['0'],
# 'content': ['POSTテスト'],
# 'attachments-TOTAL_FORMS': ['3'],
# 'attachments-INITIAL_FORMS': ['0'],
# 'attachments-MIN_NUM_FORMS': ['0'],
# 'attachments-MAX_NUM_FORMS': ['6'],
# 'attachments-0-attachment_file': [''],
# 'attachments-0-id': [''],
# 'attachments-0-message': [''],
# 'attachments-1-attachment_file': [''],
# 'attachments-1-id': [''],
# 'attachments-1-message': [''],
# 'attachments-2-attachment_file': [''],
# 'attachments-2-id': [''],
# 'attachments-2-message': [''],
# 'SEND': ['送信']
# }

    def test_send_POST_logOUT(self):
        data = {
            'title': ['LogOUT POST test'],
            'year_choice': ['2019'],
            'written_by': ['2019-1'],
            'to': ['0'],
            'content': ['LogOUT POST test message'],
            'attachments-TOTAL_FORMS': ['3'],
            'attachments-INITIAL_FORMS': ['0'],
            'attachments-MIN_NUM_FORMS': ['0'],
            'attachments-MAX_NUM_FORMS': ['6'],
            'attachments-0-attachment_file': [''],
            'attachments-0-id': [''],
            'attachments-0-message': [''],
            'attachments-1-attachment_file': [''],
            'attachments-1-id': [''],
            'attachments-1-message': [''],
            'attachments-2-attachment_file': [''],
            'attachments-2-id': [''],
            'attachments-2-message': [''],
            }
        User_LogOUT(self)
        request = self.client.post('/send/', data)
        self.assertEqual(request.status_code, 302)
        url_redial_to = request.url
        response = self.client.get(url_redial_to)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin/login.html')

        try:
            saved_content = Message.objects.get(title=data['title'][0])
            self.assertTrue(False)
        except ObjectDoesNotExist:
            self.assertTrue(True)
        

    def test_send_POST_logIN(self):
        user = User_LogIN(self)
        data = {
            'title': ['LogIN POST test'],
            'year_choice': [str(user.year)],
            'written_by': [str(user.year).zfill(4) + '-' + str(user.pk)],
            'to': ['0'],
            'content': ['LogIN POST test message'],
            'attachments-TOTAL_FORMS': ['3'],
            'attachments-INITIAL_FORMS': ['0'],
            'attachments-MIN_NUM_FORMS': ['0'],
            'attachments-MAX_NUM_FORMS': ['6'],
            'attachments-0-attachment_file': [''],
            'attachments-0-id': [''],
            'attachments-0-message': [''],
            'attachments-1-attachment_file': [''],
            'attachments-1-id': [''],
            'attachments-1-message': [''],
            'attachments-2-attachment_file': [''],
            'attachments-2-id': [''],
            'attachments-2-message': [''],
        }
        request = self.client.post('/send/', data)
        self.assertEqual(request.status_code, 302)
        url_redial_to = request.url
        self.assertEqual(url_redial_to, '../read/')

        response = self.client.get('/read/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, data['title'][0])
        
        saved_content = Message.objects.get(title=data['title'][0])
        target = '/read/content/' + str(saved_content.pk)
        response = self.client.get(target)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, data['content'][0])

    def test_send_POST_logIN_missing_TITLE(self):
        data = {
            'title': [''],
            'year_choice': ['2019'],
            'written_by': ['2019-1'],
            'to': ['0'],
            'content': ['LogIN POST test message missing TITLE'],
            'attachments-TOTAL_FORMS': ['3'],
            'attachments-INITIAL_FORMS': ['0'],
            'attachments-MIN_NUM_FORMS': ['0'],
            'attachments-MAX_NUM_FORMS': ['6'],
            'attachments-0-attachment_file': [''],
            'attachments-0-id': [''],
            'attachments-0-message': [''],
            'attachments-1-attachment_file': [''],
            'attachments-1-id': [''],
            'attachments-1-message': [''],
            'attachments-2-attachment_file': [''],
            'attachments-2-id': [''],
            'attachments-2-message': [''],
        }
        User_LogIN(self)
        request = self.client.post('/send/', data)
        self.assertEqual(request.status_code, 200)
        self.assertTemplateUsed(request, 'board/send.html')
        self.assertContains(request, validation_error_messages['no_title'])
        try:
            saved_content = Message.objects.get(title=data['title'][0])
            self.assertTrue(False)
        except ObjectDoesNotExist:
            self.assertTrue(True)

    def test_send_POST_logIN_missing_CONTENT(self):
        data = {
            'title': ['LogIN POST test missing CONTENT'],
            'year_choice': ['2019'],
            'written_by': ['2019-1'],
            'to': ['0'],
            'content': [''],
            'attachments-TOTAL_FORMS': ['3'],
            'attachments-INITIAL_FORMS': ['0'],
            'attachments-MIN_NUM_FORMS': ['0'],
            'attachments-MAX_NUM_FORMS': ['6'],
        }
        User_LogIN(self)
        request = self.client.post('/send/', data)
        self.assertEqual(request.status_code, 200)
        self.assertTemplateUsed(request, 'board/send.html')
        self.assertContains(request, validation_error_messages['no_content'])
        try:
            saved_content = Message.objects.get(title=data['title'][0])
            self.assertTrue(False)
        except ObjectDoesNotExist:
            self.assertTrue(True)

    def test_send_POST_logIN_missing_writtenby(self):
        data = {
            'title': ['LogIN POST test missing Written By'],
            'year_choice': ['2019'],
            'written_by': [''],
            'to': ['0'],
            'content': ['LogIN POST test missing Written By content'],
            'attachments-TOTAL_FORMS': ['3'],
            'attachments-INITIAL_FORMS': ['0'],
            'attachments-MIN_NUM_FORMS': ['0'],
            'attachments-MAX_NUM_FORMS': ['6'],
        }
        User_LogIN(self)
        request = self.client.post('/send/', data)
        self.assertEqual(request.status_code, 200)
        self.assertTemplateUsed(request, 'board/send.html')
        self.assertContains(request, validation_error_messages['no_writer'])
        try:
            saved_content = Message.objects.get(title=data['title'][0])
            self.assertTrue(False)
        except ObjectDoesNotExist:
            self.assertTrue(True)

    def test_send_POST_logIN_no_year_choice(self):
        data = {
            'title': ['LogIN POST test no year choice'],
            'year_choice': [''],
            'written_by': ['2019-1'],
            'to': ['0'],
            'content': ['LogIN POST test no year choice content'],
            'attachments-TOTAL_FORMS': ['3'],
            'attachments-INITIAL_FORMS': ['0'],
            'attachments-MIN_NUM_FORMS': ['0'],
            'attachments-MAX_NUM_FORMS': ['6'],
        }
        User_LogIN(self)
        request = self.client.post('/send/', data)
        self.assertEqual(request.status_code, 302)
        url_redial_to = request.url
        self.assertEqual(url_redial_to, '../read/')

        response = self.client.get('/read/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, data['title'][0])
        
        saved_content = Message.objects.get(title=data['title'][0])
        target = '/read/content/' + str(saved_content.pk)
        response = self.client.get(target)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, data['content'][0])


    def test_send_POST_logIN_with_TextFile(self):
        self.testfiles = [['29MB.txt', 29*1024*1024], ['31MB.txt', 31*1024*1024]]
        user = User_LogIN(self)
        for textfile in self.testfiles:
            filedir = os.path.join(BASE_DIR, 'board', textfile[0])
            with open(filedir, 'rb') as file:
                data = {
                    'title': ['LogIN POST test with' + textfile[0]],
                    'year_choice': [str(user.year)],
                    'written_by': [str(user.year).zfill(4) + '-' + str(user.pk)],
                    'to': ['0'],
                    'content': ['LogIN POST test with' + textfile[0]],
                    'attachments-TOTAL_FORMS': ['3'],
                    'attachments-INITIAL_FORMS': ['0'],
                    'attachments-MIN_NUM_FORMS': ['0'],
                    'attachments-MAX_NUM_FORMS': ['6'],
                    'attachments-0-attachment_file': [SimpleUploadedFile(textfile[0], file.read())],
                }
                request = self.client.post('/send/', data)
                if textfile[1] < 30*1024*1024:
                    self.assertEqual(request.status_code, 302) # => 成功、read/へ転送
                    url_redial_to = request.url
                    self.assertEqual(url_redial_to, '../read/')

                    response = self.client.get('/read/')
                    self.assertEqual(response.status_code, 200)
                    self.assertContains(response, data['title'][0])
                    
                    saved_content = Message.objects.get(title=data['title'][0])
                    target = '/read/content/' + str(saved_content.pk)
                    response = self.client.get(target)
                    self.assertEqual(response.status_code, 200)
                    self.assertContains(response, data['content'][0])
                    self.assertContains(response, data['title'][0] + '_添付')

                else:
                    self.assertEqual(request.status_code, 200) # => 失敗、sendにとどまる
                    self.assertTemplateUsed(request, 'board/send.html')
                    self.assertContains(request, data['title'][0])
                    self.assertContains(request, 'どの添付ファイルのサイズも30MB未満にしてください')
                    try:
                        saved_content = Message.objects.get(title=data['title'][0])
                        self.assertTrue(False)
                    except ObjectDoesNotExist:
                        self.assertTrue(True)

    def test_send_POST_logIN_multiple_send_to(self):
        send_to = ['2018', '2019']
        data = {
            'title': ['LogIN POST test mutiple send to'],
            'year_choice': [''],
            'written_by': ['2019-1'],
            'to': send_to,
            'content': ['LogIN POST test mutiple send to content'],
            'attachments-TOTAL_FORMS': ['3'],
            'attachments-INITIAL_FORMS': ['0'],
            'attachments-MIN_NUM_FORMS': ['0'],
            'attachments-MAX_NUM_FORMS': ['6'],
        }
        User_LogIN(self)
        request = self.client.post('/send/', data)
        self.assertEqual(request.status_code, 302)
        url_redial_to = request.url
        self.assertEqual(url_redial_to, '../read/')

        response = self.client.get('/read/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, data['title'][0])
        
        saved_content = Message.objects.get(title=data['title'][0])
        target = '/read/content/' + str(saved_content.pk)
        response = self.client.get(target)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, data['content'][0])

    def test_send_POST_logIN_with_multiple_TextFile(self):
        self.testfiles = ['1KB.txt', '2KB.txt', '4KB.txt']
        user = User_LogIN(self)
        filedir = [os.path.join(BASE_DIR, 'board', testfile) for testfile in self.testfiles]
        with open(filedir[0], 'rb') as file0:
            with open(filedir[1], 'rb') as file1:
                with open(filedir[2], 'rb') as file2:
                    data = {
                        'title': ['LogIN POST test with multiple TextFile'],
                        'year_choice': [str(user.year)],
                        'written_by': [str(user.year).zfill(4) + '-' + str(user.pk)],
                        'to': ['0'],
                        'content': ['LogIN POST test with multiple TextFile'],
                        'attachments-TOTAL_FORMS': ['3'],
                        'attachments-INITIAL_FORMS': ['0'],
                        'attachments-MIN_NUM_FORMS': ['0'],
                        'attachments-MAX_NUM_FORMS': ['6'],
                        'attachments-0-attachment_file': [SimpleUploadedFile(self.testfiles[0], file0.read())],
                        'attachments-1-attachment_file': [SimpleUploadedFile(self.testfiles[1], file1.read())],
                        'attachments-2-attachment_file': [SimpleUploadedFile(self.testfiles[2], file2.read())],
                    }
                    request = self.client.post('/send/', data)

        self.assertEqual(request.status_code, 302) # => 成功、read/へ転送
        url_redial_to = request.url
        self.assertEqual(url_redial_to, '../read/')

        response = self.client.get('/read/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, data['title'][0])
        
        saved_content = Message.objects.get(title=data['title'][0])
        target = '/read/content/' + str(saved_content.pk)
        response = self.client.get(target)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, data['content'][0])
        self.assertContains(response, data['title'][0] + '_添付1')
        self.assertContains(response, data['title'][0] + '_添付2')
        self.assertContains(response, data['title'][0] + '_添付3')

    def test_send_POST_logIN_with_multiple_TextFile_FileSizeOVER(self):
        self.testfiles = ['1KB.txt', '2KB.txt', '31MB.txt']
        user = User_LogIN(self)
        filedir = [os.path.join(BASE_DIR, 'board', testfile) for testfile in self.testfiles]
        with open(filedir[0], 'rb') as file0:
            with open(filedir[1], 'rb') as file1:
                with open(filedir[2], 'rb') as file2:
                    data = {
                        'title': ['LogIN POST test with multiple TextFile'],
                        'year_choice': [str(user.year)],
                        'written_by': [str(user.year).zfill(4) + '-' + str(user.pk)],
                        'to': ['0'],
                        'content': ['LogIN POST test with multiple TextFile'],
                        'attachments-TOTAL_FORMS': ['3'],
                        'attachments-INITIAL_FORMS': ['0'],
                        'attachments-MIN_NUM_FORMS': ['0'],
                        'attachments-MAX_NUM_FORMS': ['6'],
                        'attachments-0-attachment_file': [SimpleUploadedFile(self.testfiles[0], file0.read())],
                        'attachments-1-attachment_file': [SimpleUploadedFile(self.testfiles[1], file1.read())],
                        'attachments-2-attachment_file': [SimpleUploadedFile(self.testfiles[2], file2.read())],
                    }
                    request = self.client.post('/send/', data)

        self.assertEqual(request.status_code, 200) # => 失敗、sendにとどまる
        self.assertTemplateUsed(request, 'board/send.html')
        self.assertContains(request, data['title'][0])
        self.assertContains(request, 'どの添付ファイルのサイズも30MB未満にしてください')
        try:
            saved_content = Message.objects.get(title=data['title'][0])
            self.assertTrue(False)
        except ObjectDoesNotExist:
            self.assertTrue(True)