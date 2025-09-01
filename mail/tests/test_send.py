from django.test import TestCase
from django.urls import reverse
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from members.models import User
from mail.models import ToGroup


class SendViewTests(TestCase):
    def setUp(self):
        # ユーザーを作成
        self.user = User.objects.create_user(
            email="testuser@example.com",
            year=2025,
        )
        self.user.fullname = "テストユーザー"
        self.user.furigana = "てすと"
        self.user.save()
        self.send_url = reverse("mail:send")

    def test_send_view_redirects_if_not_logged_in(self):
        """
        未ログインユーザーはメール送信ページにアクセスすると
        ログインページへリダイレクトされること
        """
        response = self.client.get(self.send_url)
        self.assertEqual(response.status_code, 302)
        expected_redirect = f"{settings.LOGIN_URL}?next={self.send_url}"
        self.assertRedirects(response, expected_redirect, fetch_redirect_response=False)

    def test_send_view_accessible_for_logged_in_user(self):
        """
        ログイン済みユーザーはメール送信ページにアクセスできること
        """
        self.client.force_login(self.user)
        response = self.client.get(self.send_url)
        self.assertEqual(response.status_code, 200)

    def test_send_redirects_to_first_register_if_user_incomplete(self):
        """
        fullnameとfuriganaが未設定の場合first_registerにリダイレクトされること
        """
        incomplete_user = User.objects.create_user(
            email="incomplete@example.com",
            year=2025,
        )
        # fullnameとfuriganaを設定しない
        self.client.force_login(incomplete_user)
        response = self.client.get(self.send_url)
        expected_url = reverse("members:first_register")
        self.assertRedirects(response, expected_url, fetch_redirect_response=False)

    def test_send_create_fill_form(self):
        """
        メール送信フォームに必要項目を入力し、POSTすると確認画面に遷移すること
        """
        # グループ作成
        group = ToGroup.objects.create(year=2025, label="2025年度メンバー")
        self.client.force_login(self.user)

        # 初期表示でmanagement_formとフォーム情報を取得
        response = self.client.get(self.send_url)
        wizard = response.context["wizard"]
        management_form = wizard["management_form"]
        message_form = response.context["message_form"]
        attachment_formset = response.context["attachment_formset"]

        # wizard管理用データ
        post_data = {"send_wizard_view-current_step": "compose"}
        post_data.update(
            {
                "writer": str(self.user.id),
                "to_groups": [str(group.id)],
                "title": "テスト件名",
                "content": "テスト本文",
            }
        )

        # message_formデータ
        post_data.update(
            {
                "writer": str(self.user.id),
                "to_groups": [str(group.id)],
                "title": "テスト件名",
                "content": "テスト本文",
                "message_form-title": "テスト件名",
                "message_form-content": "テスト本文",
                "message_form-writer": str(self.user.id),
                "message_form-to_groups": [str(group.id)],
            }
        )

        # attachment_formset管理用データ
        for field in attachment_formset.management_form.hidden_fields():
            post_data[field.name] = field.value()

        # 添付ファイルを作成（3バイト以上で有効）
        file_data = SimpleUploadedFile("test.txt", b"abc")
        files = {f"{attachment_formset.prefix}-0-file": file_data}

        # POSTして確認ステップに遷移
        response2 = self.client.post(self.send_url, data=post_data, files=files)
        self.assertEqual(response2.status_code, 200)
        self.assertTemplateUsed(response2, "mail/send_create.html")
