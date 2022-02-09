import os
import datetime

from django.test import TestCase, Client
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import Permission

from django.conf import settings

from members.models import User
from .models import Kansouyoushi


def user_logout(self):
    self.client = Client()
    self.client.logout()


def make_a_user(self, year=2019):
    self.user = User.objects.create_user(email=str(year) + "mail@gmail.com", year=year)
    self.user.last_name = "京大"
    self.user.first_name = "太郎"
    self.user.furigana = "きょうだいたろう"
    self.user.save()
    return self.user


def make_a_staff_user(self, year=2019):
    self.user = make_a_user(self, year)
    self.user.is_staff = True
    self.user.save()
    return self.user


def user_login(self, year=2019):
    self.client.force_login(User.objects.get(email=str(year) + "mail@gmail.com"))


def user_login_and_give_permission(self, year=2019):
    user = User.objects.get(email=str(year) + "mail@gmail.com")
    permission = Permission.objects.get(codename="add_kansouyoushi")
    user.user_permissions.add(permission)
    self.client.force_login(user)


def make_kansou(self, user_year=2019, performed_at=datetime.date.today()):
    Kansouyoushi.objects.all().delete()
    pdfdir = os.path.join(settings.BASE_DIR, "kansou", "test.pdf")
    filename = "テスト感想用紙.pdf"
    with open(pdfdir, "rb") as file:
        Kansouyoushi.objects.create(
            title="テストライブ",
            detail="テストの分です",
            file=SimpleUploadedFile(filename, file.read()),
            performed_at=performed_at,
            created_by=User.objects.get(email=str(user_year) + "mail@gmail.com"),
            created_at=datetime.datetime.now()
        )


class KansouViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        make_a_user(cls)

    def test_get_kansou_admin_logOUT(self):
        user_logout(self)
        response = self.client.get("/api/kansou/")
        self.assertEqual(response.status_code, 302)

    def test_get_kansou_api_logIN(self):
        user_login(self)
        make_kansou(self)
        response = self.client.get("/api/kansou/")
        self.assertEqual(response.status_code, 200)

    def test_file_exists(self):
        make_kansou(self)
        today = datetime.date.today()
        filepath = os.path.join(
            settings.BASE_DIR, "private_media", "kansou",
            today.strftime("%Y"), today.strftime("%Y%m%d") + ".pdf")
        self.assertTrue(os.path.isfile(filepath))


class KansouAdminTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        make_a_staff_user(cls)

    def test_kansou_admin_login_without_permission(self):
        user_login(self)
        response = self.client.get("/admin/kansou/kansouyoushi/add/")
        self.assertEqual(response.status_code, 403)

    def test_kansou_admin_login_with_permission(self):
        # 初め、感想用紙が存在しないことを確認
        self.assertFalse(Kansouyoushi.objects.all().exists())
        
        user_login_and_give_permission(self)
        response = self.client.get("/admin/kansou/kansouyoushi/add/")
        self.assertEqual(response.status_code, 200)

        filedir = os.path.join(settings.BASE_DIR, "kansou", "test.pdf")
        with open(filedir, "rb") as file:
            data = {
                "title": "テストライブ",
                "performed_at": datetime.date.today(),
                "file": SimpleUploadedFile("test.pdf", file.read()),
            }
            request = self.client.post("/admin/kansou/kansouyoushi/add/", data)
        
        self.assertEqual(request.status_code, 302)

        # 感想用紙が存在することを確認
        kansou = Kansouyoushi.objects.get(performed_at=data["performed_at"])
        self.assertEqual(kansou.title, data["title"])

        # 感想用紙が指定されたディレクトリに存在することを確認
        performed_at = data["performed_at"]
        filepath = os.path.join(
            settings.BASE_DIR, "private_media", "kansou",
            performed_at.strftime("%Y"), performed_at.strftime("%Y%m%d") + ".pdf")
        self.assertTrue(os.path.isfile(filepath))
