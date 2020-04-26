from django.test import TestCase, Client
from members.models import User


def User_LogOUT(self):
    self.client = Client()
    self.client.logout()

def Make_User(self,year=2019):
    self.user = User.objects.create_user(
        email=str(year) + 'mail@gmail.com',
        year=year)
    self.user.last_name = '京大'
    self.user.first_name = '太郎'
    self.user.furigana = 'きょうだいたろう'
    self.user.save()
    return self.user

def User_LogIN(self,year=2019):
    self.user = User.objects.get(email=str(year) + 'mail@gmail.com')
    self.client.force_login(self.user)
    return self.user


class OtherDocumentsViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Make_User(cls)

    def test_other_docs_view_logOUT(self):
        User_LogOUT(self)        
        response = self.client.get('/others/')
        self.assertEqual(response.status_code, 302)
        url_redial_to = response.url
        response = self.client.get(url_redial_to)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin/login.html')

    def test_other_docs_view_logIN(self):
        User_LogIN(self)
        response = self.client.get('/others/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'otherdocs/index.html')