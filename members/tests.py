from django.test import TestCase, Client
from django.db.models import Count
from members.models import User
import os
import datetime


def User_LogOUT(self):
    self.client = Client()
    self.client.logout()

def Make_User(self,year=2019):
    self.user = User.objects.create_user(email=str(year) + 'mail@gmail.com', year=year)
    return self.user

def User_LogIN(self,year=2019):
    self.user = User.objects.get(email=str(year) + 'mail@gmail.com')
    self.client.force_login(self.user)
    return self.user


class MemberRegisterFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Make_User(cls)


    def test_members_index_logOUT(self):
        User_LogOUT(self)
        response = self.client.get('/members/')
        self.assertEqual(response.status_code, 302)
        url_redial_to = response.url
        response = self.client.get(url_redial_to)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin/login.html')

    def test_members_index_logIN(self):
        User_LogIN(self)
        response = self.client.get('/members/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'members/index.html')

    def test_members_update_logOUT(self):
        User_LogOUT(self)
        response = self.client.get('/members/update/')
        self.assertEqual(response.status_code, 302)
        url_redial_to = response.url
        response = self.client.get(url_redial_to)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin/login.html')

    def test_members_update_logIN(self):
        User_LogIN(self)
        response = self.client.get('/members/update/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'members/mypage_UserUpdate.html')

    def test_members_update_logIN(self):
        data = {
            'last_name': '京大',
            'first_name': '太郎',
            'furigana': 'きょうだいたろう',
            'nickname': 'タロー',
        }
        self.user = User_LogIN(self)
        request = self.client.post('/members/update/', data)
        self.assertEqual(request.status_code, 302)
        url_redial_to = request.url
        self.assertEqual(url_redial_to, '/members')

        response = self.client.get('/members/update/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, data['last_name'])

        updated_user = User.objects.get(pk=self.user.pk)
        self.assertTrue(updated_user.last_name == data['last_name'])
        self.assertTrue(updated_user.first_name == data['first_name'])
        self.assertTrue(updated_user.furigana == data['furigana'])
        self.assertTrue(updated_user.nickname == data['nickname'])

