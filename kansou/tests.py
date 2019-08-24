from django.test import TestCase, Client
from members.models import User

def User_LogOUT(self):
    self.client = Client()
    self.client.logout()

def Make_User_and_LogIN(self,year=2019):
    self.user = User.objects.create_user(email=str(year) + 'mail@gmail.com', year=year, password='hogehoge')
    self.client = Client()
    self.client.force_login(self.user)

def User_LogIN(self,year=2019):
    self.client.force_login(User.objects.get(email=str(year) + 'mail@gmail.com'))

class KansouyoushiViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass


    def test_read_index_logOUT(self):
        User_LogOUT(self)
        response = self.client.get('/kansou/')
        self.assertEqual(response.status_code, 302)
        url_redial_to = response.url
        response = self.client.get(url_redial_to)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin/login.html')