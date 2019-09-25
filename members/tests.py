from django.test import TestCase, Client
from django.db.models import Count
from members.models import User
from django.contrib.auth.models import Group
import os
import datetime
from django.core.exceptions import ObjectDoesNotExist


def User_LogOUT(self):
    self.client = Client()
    self.client.logout()

def Make_User(self,year=2019):
    self.user = User.objects.create_user(email=str(year) + 'mail@gmail.com', year=year)
    return self.user

def User_LogIN_and_Add_AdministerGroup(self,year=2019):
    user = User.objects.get(email=str(year) + 'mail@gmail.com')
    admin_group = Group.objects.create(name='Administer')
    admin_group.user_set.add(user)
    self.client.force_login(user)
    return user

def User_LogIN(self,year=2019):
    self.user = User.objects.get(email=str(year) + 'mail@gmail.com')
    self.client.force_login(self.user)
    return self.user


class MemberUpdateFormTest(TestCase):
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

    def test_members_update_POST_logOUT(self):
        data = {
            'last_name': '京大',
            'first_name': '太郎',
            'furigana': 'きょうだいたろう',
            'nickname': 'タロー',
        }
        User_LogOUT(self)
        request = self.client.post('/members/update/', data)
        self.assertEqual(request.status_code, 302)
        url_redial_to = request.url
        response = self.client.get(url_redial_to)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin/login.html')

        try:
            saved_content = User.objects.get(last_name=data['last_name'])
            self.assertTrue(False)
        except ObjectDoesNotExist:
            self.assertTrue(True)


    def test_members_update_POST_logIN(self):
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



class MemberRegisterFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Make_User(cls)

    def test_members_Register_FORM_POST_NoSuperuser_logIN(self):
        data = {
            'email': '2019tryaddinguser@gmail.com',
            'year': 2019,
            'last_name': '京大',
            'first_name': '太郎',
            'furigana': 'きょうだいたろう',
            'nickname': 'タロー',
        }
        User_LogIN(self)
        request = self.client.post('/members/register/', data)
        self.assertEqual(request.status_code, 302)
        url_redial_to = request.url
        self.assertEqual(url_redial_to, '/members')        
        response = self.client.get(url_redial_to)
        # print(response)
        # self.assertEqual(response.status_code, 301)
        # self.assertTemplateUsed(response, 'members/index.html')
        try:
            saved_content = User.objects.get(email=data['email'])
            self.assertTrue(False)
        except ObjectDoesNotExist:
            self.assertTrue(True)


    def test_members_Register_FORM_POST_logIN(self):
        data = {
        	'email': '2019addeduser@gmail.com',
        	'year': 2019,
            'last_name': '京大',
            'first_name': '太郎',
            'furigana': 'きょうだいたろう',
            'nickname': 'タロー',
        }
        self.user = User_LogIN_and_Add_AdministerGroup(self)
        request = self.client.post('/members/register/', data)

        self.assertEqual(request.status_code, 200)
        self.assertContains(request, data['email'])
        self.assertTemplateUsed(request, 'members/register.html')

        created_user = User.objects.get(email=data['email'])
        self.assertTrue(created_user.last_name == data['last_name'])
        self.assertTrue(created_user.first_name == data['first_name'])
        self.assertTrue(created_user.furigana == data['furigana'])
        self.assertTrue(created_user.nickname == '')


class MemberRegisterCSVFileTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Make_User(cls)

        def test_members_Register_CSV_Register_logOUT(self):
            pass
        def test_members_Register_CSV_Register_NoSuperuser_logIN(self):
            pass
        def test_members_Register_CSV_Register_Superuser_LogIN(self):
            pass