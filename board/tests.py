import os
import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, Client, override_settings

from django.conf import settings
from members.models import User
from .models import Message, MessageYear, ToGroup


def make_user(self, year=2019):
    self.user = User.objects.create_user(
        email=str(year) + 'mail@gmail.com',
        year=year
        )
    self.user.last_name = '京大'
    self.user.first_name = '太郎'
    self.user.furigana = 'きょうだいたろう'
    self.user.save()
    return self.user

def login(self, user):
    self.client = Client()
    self.client.force_login(user)
    return user

def logout(self):
    self.client = Client()
    self.client.logout()

def make_message(self, year=2019, is_attachment=False):
    nowtime = datetime.datetime.now()
    user = User.objects.get(email=str(year) + 'mail@gmail.com')
    for messageyear in [0,year]: # 全回と回生の２件を作る
        content_data = Message(
            title=str(messageyear),
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

def URLS(id=1):
    return [
        '/read/',
        '/send/',
        '/api/board/json/',
        '/api/board/content/{}/'.format(id),
        '/api/board/contentothers/{}/'.format(id),
        '/api/board/bookmark/{}/'.format(id),
        '/api/board/send/togroups/',
        '/api/board/send/froms/',
        '/api/board/send/send/',
    ]
YEARS = (2017,2018,2019)

def create_togroup(self, year):
    obj = ToGroup(year=year)
    obj.save()


@override_settings(SEND_MAIL=False)
class LoginLogoutTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        for year in YEARS:
            make_user(cls, year=year)

    def test_SPA_logOUT(self):
        logout(self)
        for url in URLS():
            response = self.client.get(url)
            self.assertEqual(response.status_code, 302)
            url_redial_to = response.url
            response = self.client.get(url_redial_to)
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, 'admin/login.html')

    def test_SPA_logIN(self):
        for year in YEARS:
            user = User.objects.get(email=str(year) + 'mail@gmail.com')
            login(self, user=user)
            response = self.client.get('/read/')
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, 'SPA.html')
            response = self.client.get('/send/')
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, 'SPA.html')
            logout(self)


@override_settings(SEND_MAIL=False)
class APIReadTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        for year in YEARS:
            make_user(cls, year=year)
            make_message(cls, year=year)
            create_togroup(cls, year=year)

    def test_read_index_api(self):
        """
        indexで正しいメーリスのjsonが返されているかテスト
        """
        for year in YEARS:
            user = User.objects.get(email=str(year) + 'mail@gmail.com')
            login(self, user=user)
            response = self.client.get('/api/board/json/')
            content = response.json()
            for message in content['message_list']:
                # 全回か、userの回生メーリスが含まれている
                self.assertIn(message['title'], ['0', str(year)])
                # それ以外の回生メーリスは含まれていない
                # print([y for y in YEARS if y != year])
                self.assertNotIn(message['title'], [y for y in YEARS if y != year])

    def test_read_content_api(self):
        """
        contentで正しくメーリスのjsonが返されているかテスト
        """
        for year in YEARS:
            user = User.objects.get(email=str(year) + 'mail@gmail.com')
            login(self, user=user)
            for message in Message.objects.all():
                response = self.client.get('/api/board/content/{}/'.format(message.id))
                if response.status_code == 200:
                    content = response.json()
                    data = content['message']
                    # 全回か、userの回生メーリスが含まれている
                    self.assertIn(data['title'], ['0', str(year)])
                    # それ以外の回生メーリスは含まれていない
                    self.assertNotIn(data['title'], [str(y) for y in YEARS if y != year])
                elif response.status_code == 403:
                    # 403を受けるのは全回ではなく、回生でも無い場合
                    self.assertNotIn(message.title, ['0', str(year)])
                else:
                    self.assertTrue(False)


    def test_read_attachment_api(self):
        """
        添付ファイルのjsonに正しくアクセスできるかテスト
        """
        for year in YEARS:
            user = User.objects.get(email=str(year) + 'mail@gmail.com')
            login(self, user=user)
            for message in Message.objects.all():
                
                with open(os.path.join(settings.BASE_DIR, 'board', '1KB.txt'), 'rb') as f:
                    file = SimpleUploadedFile('1KB.txt', f.read())
                message.attachments.create(attachment_file=file)

                response = self.client.get('/api/board/contentothers/{}/'.format(message.id))
                if response.status_code == 200:
                    content = response.json()
                    # data = content['message']
                    # 全回か、userの回生メーリスが含まれている
                    self.assertIn(message.title, ['0', str(year)])
                    # それ以外の回生メーリスは含まれていない
                    self.assertNotIn(message.title, [str(y) for y in YEARS if y != year])
                elif response.status_code == 403:
                    # 403を受けるのは全回ではなく、回生でも無い場合
                    self.assertNotIn(message.title, ['0', str(year)])
                else:
                    self.assertTrue(False)


@override_settings(SEND_MAIL=False)
class APISendTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        for year in YEARS:
            create_togroup(cls, year=year)
    
    def test_sendAPI_kaisei_without_attachment(self):
        user = make_user(self, year=2019)
        login(self, user)

        __sendyears = [[2019], [2018], [2017], [2019, 2018], [2019, 2018, 2017]]
        for sendyear in __sendyears:
            data = {
                "title": ["send test title" + str(sendyear)],
                "writer": [str(user.id)],
                "to": [y for y in sendyear],
                "content": ["send text content"]
            }
            request = self.client.post('/api/board/send/send/', data)

            self.assertEqual(request.status_code, 200)
           
            new_message = Message.objects.get(title=data["title"][0])
            self.assertEqual(new_message.content, data['content'][0])
            years = MessageYear.objects.filter(message=new_message).values_list('year', flat=True)
            for y in sendyear:
                self.assertIn(y, years)
                
    def test_sendAPI_kaisei_INVALID_request(self):
        user = make_user(self, year=2019)
        login(self, user)

        __sendyears = [[2019], [2018], [2017], [2019, 2018], [2019, 2018, 2017]]
        for sendyear in __sendyears:
            data = {
                "title": ["no content test" + str(sendyear)],
                "writer": [str(user.id)],
                "to": [y for y in sendyear],
                "content": [""]
            }
            request = self.client.post('/api/board/send/send/', data)
            self.assertEqual(request.status_code, 400)
            self.assertFalse(
                Message.objects.filter(title=data["title"]).exists()
                )

            data = {
                "title": [""],
                "writer": [str(user.id)],
                "to": [y for y in sendyear],
                "content": ["no title test"]
            }
            request = self.client.post('/api/board/send/send/', data)
            self.assertEqual(request.status_code, 400)
            self.assertFalse(
                Message.objects.filter(content=data["content"]).exists()
                )

            data = {
                "title": ["no writer test"],
                "writer": "",
                "to": [y for y in sendyear],
                "content": ["no writer test"]
            }
            request = self.client.post('/api/board/send/send/', data)
            self.assertEqual(request.status_code, 400)
            self.assertFalse(
                Message.objects.filter(title=data["title"]).exists()
                )

            data = {
                "title": ["no 'to' test"],
                "writer": "str(user.id)",
                "to": "",
                "content": ["no 'to' test"]
            }
            request = self.client.post('/api/board/send/send/', data)
            self.assertEqual(request.status_code, 400)
            self.assertFalse(
                Message.objects.filter(title=data["title"]).exists()
                )

    
    def test_sendAPI_kaisei_with_attachment(self):
        user = make_user(self, year=2019)
        login(self, user)

        __sendyears = [[2019], [2018], [2017], [2019, 2018], [2019, 2018, 2017]]
        __testfiles = [
            ('0B.txt', 0),
            ('9MB.txt', 9*1024*1024),
            ('11MB.txt', 11*1024*1024)
            ]
        for sendyear in __sendyears:
            for file in __testfiles:
                with open(
                    os.path.join(settings.BASE_DIR, 'board', file[0]),
                    'rb') as f:
                    upload = SimpleUploadedFile(file[0], f.read())
                data = {
                    "title": ["attachment test" + file[0] + str(sendyear)],
                    "writer": [str(user.id)],
                    "to": [y for y in sendyear],
                    "content": ["send text content"],
                    "attachment_file": [upload]
                }
                request = self.client.post('/api/board/send/send/', data)

                if 0 < file[1] < 10*1000*1000:
                    self.assertEqual(request.status_code, 200)
                    new_message = Message.objects.get(title=data["title"][0])
                    self.assertEqual(new_message.content, data['content'][0])
                    years = MessageYear.objects.filter(message=new_message).values_list('year', flat=True)
                    for y in sendyear:
                        self.assertIn(y, years)
                    for y in years:
                        self.assertIn(y, sendyear)

                    # 添付ファイルのmodelが作られているか
                    self.assertTrue(new_message.attachments.exists())

                else:
                    self.assertEqual(request.status_code, 400)
                    self.assertFalse(
                        Message.objects.filter(title=data["title"]).exists()
                        )



    # def test_sendAPI_kaisei_with_two_attachments(self):
    #     user = make_user(self, year=2019)
    #     login(self, user)

    #     __sendyears = [[2019], [2018], [2017], [2019, 2018], [2019, 2018, 2017]]
    #     __testfiles = [
    #           [('0B.txt', 0),('0B.txt', 0)],
    #           [('1KB.txt', 1024),('1KB.txt', 1024)],
    #           [('9MB.txt', 9*1024*1024),('1KB.txt', 1024)],
    #           [('11MB.txt', 11*1024*1024),('1KB.txt', 1024)],
    #           [('4KB.txt', 4*1024),('0B.txt', 0)],
    #           [('9MB.txt', 9*1024*1024),('9MB.txt', 9*1024*1024)],
    #         ]
    #     for sendyear in __sendyears:
    #         for files in __testfiles:
    #             with open(
    #                 os.path.join(settings.BASE_DIR, 'board', files[0][0]),
    #                 'rb') as f0:
    #                 upload0 = SimpleUploadedFile(files[0][0], f0.read())
    #             with open(
    #                 os.path.join(settings.BASE_DIR, 'board', files[1][0]),
    #                 'rb') as f1:
    #                 upload1 = SimpleUploadedFile(files[1][0], f1.read())
    #             data = {
    #                 "title": ["attachment test" + files[0][0] + files[1][0] + str(sendyear)],
    #                 "writer": [str(user.id)],
    #                 "to": [y for y in sendyear],
    #                 "content": ["send text content"],
    #                 "attachment_file": [upload0, upload1]
    #             }
    #             request = self.client.post('/api/board/send/send/', data)

    #             if 0 < files[0][1] < 10*1000*1000 and 0 < files[1][1] < 10*1000*1000\
    #               and files[0][1] + files[1][1] < 20*1024*1024:
    #                 self.assertEqual(request.status_code, 200)
    #                 new_message = Message.objects.get(title=data["title"][0])
    #                 self.assertEqual(new_message.content, data['content'][0])
    #                 years = MessageYear.objects.filter(message=new_message).values_list('year', flat=True)
    #                 for y in sendyear:
    #                     self.assertIn(y, years)
    #                 for y in years:
    #                     self.assertIn(y, sendyear)

    #                 # 添付ファイルのmodelが作られているか
    #                 self.assertTrue(new_message.attachments.exists())

    #             else:
    #                 self.assertEqual(request.status_code, 400)
    #                 self.assertFalse(
    #                     Message.objects.filter(title=data["title"]).exists()
    #                     )


