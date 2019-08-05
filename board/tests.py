from django.test import TestCase, Client
from members.models import User
import datetime
from .models import Message, MessageYear, Attachment


def User_LogOUT(self):
    self.client = Client()
    self.client.logout()

def User_LogIN(self,year=2019):
    self.user = User.objects.create_user(google_account=str(year) + 'mail@gmail.com', year=year, password='hogehoge')
    self.client = Client()
    self.client.force_login(self.user)

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



class AuthentificationViewTest(TestCase):
    def test_read_index_logOUT(self):
        User_LogOUT(self)
        response = self.client.get('/read/')
        self.assertEqual(response.status_code, 302)
        url_to = response.url
        response = self.client.get(url_to)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Google account')

    def test_read_index_logIN(self):
        User_LogIN(self)
        response = self.client.get('/read/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<title>Read</title>')

    def test_read_index_lonIN_with_content(self):
        TestYears = [y for y in range(2015,2020)]

        # Create Messages for Preparation
        for User_Year in TestYears:
            User_LogIN(self,year=User_Year)
            CreateMessage(self, year=User_Year)
            User_LogOUT(self)

        # Login Test
        for User_Year in TestYears:
            self.client.force_login(User.objects.get(google_account=str(User_Year) + 'mail@gmail.com'))
            response = self.client.get('/read/')
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, 'Title Example ' + str(User_Year)) # 同回の回生メーリスは見れているか
            self.assertContains(response, 'Title Example ' + str(0)) # 全回メーリスは見れているか
            self.assertContains(response, 'Content Example') # 詳細まで見れているか

            # 同回以外の学年を抽出
            for DeniedYear in [y for y in TestYears if y != User_Year]:
                self.assertNotContains(response, 'Title Example ' + str(DeniedYear)) # 違う学年の回生メーリスが見れていないか



