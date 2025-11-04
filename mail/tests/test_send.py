from django.test import TestCase
from django.urls import reverse
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from members.models import User
from mail.models import ToGroup, Message


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
        ログイン済みユーザーはメール送信ページへアクセスできること
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
        メール送信フォームに必要項目を入力し、Compose -> Confirm -> Complete の
        ウィザード全体の流れで Message が作成されることを検証する
        """
        # グループ作成
        group = ToGroup.objects.create(year=2025, label="2025年度メンバー")
        self.client.force_login(self.user)

        # Step 1: Compose 表示を取得して管理フォーム・フォームセットを取得
        resp1 = self.client.get(self.send_url)
        wizard = resp1.context["wizard"]
        management_form = wizard["management_form"]
        attachment_formset = resp1.context["attachment_formset"]

        # Compose ステップ用の POST データを準備
        post = {"send_wizard_view-current_step": "compose"}
        post.update(
            {
                "writer": str(self.user.id),
                "to_groups": [str(group.id)],
                "title": "テスト件名",
                "content": "テスト本文",
            }
        )

        # wizard 管理用 hidden フィールドを追加
        for field in management_form.hidden_fields():
            post[field.name] = field.value()

        # attachment formset の管理用 hidden フィールドを追加
        for field in attachment_formset.management_form.hidden_fields():
            post[field.name] = field.value()
        post["attachments-TOTAL_FORMS"] = str(attachment_formset.total_form_count())
        post["attachments-INITIAL_FORMS"] = str(attachment_formset.initial_form_count())

        # 添付ファイルを作成（3バイト以上で有効）
        file_data = SimpleUploadedFile("test.txt", b"abc")
        files = {f"{attachment_formset.prefix}-0-file": file_data}

        # Step 1 -> Step 2 (confirm) へ移行
        resp2 = self.client.post(self.send_url, data=post, files=files, follow=True)
        self.assertIn(resp2.status_code, (200, 302))
        if resp2.status_code == 200:
            self.assertTemplateUsed(resp2, "mail/send_confirm.html")

        # Step 2: Confirm 送信を実行 (Complete 実行)
        resp3 = self.client.post(
            self.send_url,
            data={"send_wizard_view-current_step": "confirm"},
            follow=True,
        )
        self.assertIn(resp3.status_code, (200, 302))

        # 送信後に Message が作成されていることを検証
        last = Message.objects.filter(sender=self.user).order_by("-id").first()
        self.assertIsNotNone(last)
        self.assertEqual(last.title, "テスト件名")
        self.assertEqual(last.content, "テスト本文")
        self.assertEqual(last.sender, self.user)
        self.assertTrue(last.to_groups.filter(id=group.id).exists())
