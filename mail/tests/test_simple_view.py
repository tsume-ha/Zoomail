from django.test import TestCase
from django.urls import reverse
from django.conf import settings  # リダイレクトURLを取得するためにsettingsをインポート
from members.models import User


class SimpleViewTests(TestCase):
    def setUp(self):
        # カスタムユーザー作成
        self.user = User.objects.create_user(email="testuser@example.com", year=2025)
        self.user.fullname = "テストユーザー"
        self.user.nickname = "テスト"
        self.user.save()

        self.inbox_url = reverse("mail:inbox")
        self.detail_url = reverse("mail:detail", kwargs={"id": 1})
        self.send_url = reverse("mail:send")
        self.login_url = settings.LOGIN_URL

    # 1. 認証が必要なビューのテスト (リダイレクトの確認)
    def test_inbox_redirects_to_login_if_not_authenticated(self):
        """ログインしていない場合はログインページへリダイレクトされる"""
        response = self.client.get(self.inbox_url)
        expected_url = f"{self.login_url}?next={self.inbox_url}"
        self.assertRedirects(response, expected_url)

    def test_detail_redirects_to_login_if_not_authenticated(self):
        """ログインしていない場合はログインページへリダイレクトされる"""
        response = self.client.get(self.detail_url)
        expected_url = f"{self.login_url}?next={self.detail_url}"
        self.assertRedirects(response, expected_url)

    def test_send_redirects_to_login_if_not_authenticated(self):
        """ログインしていない場合はログインページへリダイレクトされる"""
        response = self.client.post(self.send_url)
        expected_url = f"{self.login_url}?next={self.send_url}"
        self.assertRedirects(response, expected_url)

    # 2. ログインしている場合の正常なアクセス
    def test_inbox_success_for_authenticated_user(self):
        """ログイン済みユーザーがメール一覧にアクセスできる"""
        self.client.force_login(self.user)
        response = self.client.get(self.inbox_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "mail/inbox.html")

    def test_send_success_for_authenticated_user(self):
        """ログイン済みユーザーがメール送信画面にアクセスできる"""
        self.client.force_login(self.user)
        response = self.client.get(self.send_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "mail/send.html")

    # 3. 無効な詳細ビューリクエスト
    def test_invalid_detail_access(self):
        """無効なメールIDをリクエストした場合は404エラーを返す"""
        self.client.force_login(self.user)
        response = self.client.get(reverse("mail:detail", kwargs={"id": 9999}))
        self.assertEqual(response.status_code, 404)
