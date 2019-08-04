from django.test import TestCase, Client
from members.models import User


def User_LogOUT(self):
    self.client = Client()
    self.client.logout()

def User_LogIN(self):
    self.user = User.objects.create_user(google_account='mail@gmail.com', year=2019, password='hogehoge')
    self.client = Client()
    self.client.force_login(self.user)

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

# 許可があるユーザーだけが見ることができているか