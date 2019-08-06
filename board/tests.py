from django.test import TestCase, Client, RequestFactory
from django.db.models import Count
from members.models import User
import datetime
from .models import Message, MessageYear, Attachment


def User_LogOUT(self):
    self.client = Client()
    self.client.logout()

def Make_User_and_LogIN(self,year=2019):
    self.user = User.objects.create_user(google_account=str(year) + 'mail@gmail.com', year=year, password='hogehoge')
    self.client = Client()
    self.client.force_login(self.user)

def User_LogIN(self,year=2019):
    self.client.force_login(User.objects.get(google_account=str(year) + 'mail@gmail.com'))

def CreateMessage(self, year, is_attachment=False):
    nowtime = datetime.datetime.now()
    user = User.objects.get(google_account=str(year) + 'mail@gmail.com')
    for messageyear in [0,year]: # 全回と回生の２件を作る
        content_data = Message(
            title='Title Example ' + str(messageyear),
            content='Content Example \n'*10,
            attachment=is_attachment,
            sender_id=user,
            writer_id=user,
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


class AuthentificationViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.TestYears = [y for y in range(2015,2020)]
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
        self.assertContains(response, 'Google account')

    def test_read_index_logIN(self):
        User_LogIN(self)
        response = self.client.get('/read/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<title>Read</title>')

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
            self.assertContains(response, 'Google account')

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
                        # print('message_'+str(pk)+': 200')
                        self.assertEqual(response.status_code, 200)
                    else:
                        # print('message_'+str(pk)+': 302')
                        self.assertEqual(response.status_code, 302)
                else:
                    # print('message_'+str(pk)+': 404')
                    self.assertEqual(response.status_code, 404)

    def test_send_view_logOUT(self):
        User_LogOUT(self)
        response = self.client.get('/send/')
        self.assertEqual(response.status_code, 302)
        url_redial_to = response.url
        response = self.client.get(url_redial_to)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Google account')

    def test_send_POST_logOUT(self):
        data = {
            'title': 'NFりはの日程について',
            'to': 0,
            'content': '全回メーリス失礼します。\n\nNFリハの日程が決まりました。',
        }
        User_LogOUT(self)
        request = RequestFactory().post('/send/', data)

