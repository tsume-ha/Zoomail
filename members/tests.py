import json
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import Permission
from django.core.exceptions import ObjectDoesNotExist

from members.models import User


def User_LogOUT(self):
    self.client = Client()
    self.client.logout()


def Make_User(self, year=2019):
    self.user = User.objects.create_user(email=str(year) + "mail@gmail.com", year=year)
    self.user.last_name = "京大"
    self.user.first_name = "太郎"
    self.user.furigana = "きょうだいたろう"
    self.user.save()
    return self.user


def User_LogIN_and_Get_a_Permission(self, year=2019):
    user = User.objects.get(email=str(year) + "mail@gmail.com")
    permission = Permission.objects.get(codename="change_user")
    user.user_permissions.add(permission)
    self.client.force_login(user)
    return user


def User_LogIN(self, year=2019):
    self.user = User.objects.get(email=str(year) + "mail@gmail.com")
    self.client.force_login(self.user)
    return self.user


class MemberUpdateFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Make_User(cls)

    def test_members_index_logOUT(self):
        User_LogOUT(self)
        response = self.client.get("/members/")
        self.assertEqual(response.status_code, 302)
        url_redial_to = response.url
        response = self.client.get(url_redial_to)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "admin/login.html")

    def test_members_index_logIN(self):
        User_LogIN(self)
        response = self.client.get("/members/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "members/index.html")

    def test_members_update_logOUT(self):
        User_LogOUT(self)
        response = self.client.get("/members/update/")
        self.assertEqual(response.status_code, 302)
        url_redial_to = response.url
        response = self.client.get(url_redial_to)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "admin/login.html")

    def test_members_update_logIN(self):
        User_LogIN(self)
        response = self.client.get("/members/update/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "members/user_update.html")

    def test_members_update_POST_logOUT(self):
        data = {
            "last_name": "京大変更後",
            "first_name": "太郎変更後",
            "furigana": "きょうだいたろうへんこうご",
            "nickname": "タロー",
        }
        User_LogOUT(self)
        request = self.client.post("/members/update/", data)
        self.assertEqual(request.status_code, 302)
        url_redial_to = request.url
        response = self.client.get(url_redial_to)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "admin/login.html")

        try:
            saved_content = User.objects.get(last_name=data["last_name"])
            self.assertTrue(False)
        except ObjectDoesNotExist:
            self.assertTrue(True)

    def test_members_update_POST_logIN(self):
        data = {
            "last_name": "京大変更後",
            "first_name": "太郎変更後",
            "furigana": "きょうだいたろうへんこうご",
            "nickname": "タロー",
        }
        self.user = User_LogIN(self)
        request = self.client.post("/members/update/", data)
        self.assertEqual(request.status_code, 302)
        url_redial_to = request.url
        self.assertEqual(url_redial_to, "/members")

        response = self.client.get("/members/update/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, data["last_name"])

        updated_user = User.objects.get(pk=self.user.pk)
        self.assertTrue(updated_user.last_name == data["last_name"])
        self.assertTrue(updated_user.first_name == data["first_name"])
        self.assertTrue(updated_user.furigana == data["furigana"])
        self.assertTrue(updated_user.nickname == data["nickname"])


class MemberRegisterFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Make_User(cls)

    def test_members_Register_FORM_POST_NoSuperuser_logIN(self):
        data = {
            "email": "2019tryaddinguser@gmail.com",
            "year": 2019,
            "last_name": "京大",
            "first_name": "太郎",
            "furigana": "きょうだいたろう",
            "nickname": "タロー",
        }
        User_LogIN(self)
        request = self.client.post("/members/register/", data)
        self.assertEqual(request.status_code, 302)
        url_redial_to = request.url
        self.assertEqual(url_redial_to, "/members")
        response = self.client.get(url_redial_to)
        # print(response)
        # self.assertEqual(response.status_code, 301)
        # self.assertTemplateUsed(response, 'members/index.html')
        try:
            saved_content = User.objects.get(email=data["email"])
            self.assertTrue(False)
        except ObjectDoesNotExist:
            self.assertTrue(True)

    def test_members_Register_FORM_POST_logIN(self):
        data = {
            "email": "2019addeduser@gmail.com",
            "year": 2019,
            "last_name": "京大",
            "first_name": "太郎",
            "furigana": "きょうだいたろう",
            "nickname": "タロー",
        }
        self.user = User_LogIN_and_Get_a_Permission(self)
        request = self.client.post("/members/register/", data)

        self.assertEqual(request.status_code, 200)
        self.assertContains(request, data["email"])
        self.assertTemplateUsed(request, "members/register.html")

        created_user = User.objects.get(email=data["email"])
        self.assertTrue(created_user.last_name == data["last_name"])
        self.assertTrue(created_user.first_name == data["first_name"])
        self.assertTrue(created_user.furigana == data["furigana"])
        self.assertTrue(created_user.nickname == "")


class EmailConfirmViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Make_User(cls)

    def test_get_emailconfirm_logout(self):
        User_LogOUT(self)
        response = self.client.get(reverse("members:email_confirm"))
        self.assertEqual(response.status_code, 302)
        url_redial_to = response.url
        response = self.client.get(url_redial_to)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "admin/login.html")

    def test_get_emailconfirm_logIN(self):
        User_LogIN(self)
        response = self.client.get(reverse("members:email_confirm"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "members/email_confirm.html")


class OauthViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Make_User(cls)

    def test_get_oauth_logout(self):
        User_LogOUT(self)
        response = self.client.get(reverse("members:oauth"))
        self.assertEqual(response.status_code, 302)
        url_redial_to = response.url
        response = self.client.get(url_redial_to)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "admin/login.html")

    def test_get_oauth_logIN(self):
        User_LogIN(self)
        response = self.client.get(reverse("members:oauth"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "members/oauth_register.html")


class ApiGetUserTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Make_User(cls)

    def test_get_emailconfirm_logout(self):
        User_LogOUT(self)
        response = self.client.get(reverse("members:api_get_user"))
        self.assertEqual(response.status_code, 302)
        url_redial_to = response.url
        response = self.client.get(url_redial_to)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "admin/login.html")

    def test_get_emailconfirm_logIN(self):
        User_LogIN(self)
        response = self.client.get(reverse("members:api_get_user"))
        self.assertEqual(response.status_code, 200)
        content = json.loads(response.content)
        self.assertTrue(content["last_name"], "京大")
        self.assertTrue(content["first_name"], "太郎")
        self.assertTrue(content["furigana"], "きょうだいたろう")
