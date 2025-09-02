from django.test import TestCase
from django.urls import reverse
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from members.models import User
from mail.models import ToGroup, Message


class SendConfirmTests(TestCase):
    def setUp(self):
        # テスト用ユーザー作成
        self.user = User.objects.create_user(email="confirm@example.com", year=2025)
        self.user.fullname = "テスト送信者"
        self.user.furigana = "てすとそうし"
        self.user.save()
        self.send_url = reverse("mail:send")

    def test_confirm_and_send_creates_message(self):
        """
        コンファーム後に送信処理を実行し、Message が作成されることを検証する
        """
        # グループ作成
        group = ToGroup.objects.create(year=2025, label="2025年度メンバー")
        self.client.force_login(self.user)

        # ステップ1: Composeの表示とデータ準備
        resp1 = self.client.get(self.send_url)
        wizard = resp1.context["wizard"]
        management_form = wizard["management_form"]
        attachment_formset = resp1.context["attachment_formset"]

        post = {"send_wizard_view-current_step": "compose"}
        post.update(
            {
                "writer": str(self.user.id),
                "to_groups": [str(group.id)],
                "title": "Test Confirm",
                "content": "This is a test content for sending.",
            }
        )

        # wizard 管理データを追加
        for field in management_form.hidden_fields():
            post[field.name] = field.value()

        # 添付ファイル用の管理データを追加
        for field in attachment_formset.management_form.hidden_fields():
            post[field.name] = field.value()

        # 添付ファイル
        file_data = SimpleUploadedFile("attach.txt", b"abcd")
        files = {f"{attachment_formset.prefix}-0-file": file_data}

        # ステップ1を済ませてステップ2(確認)へ、最終送信を模擬して完了させる
        resp2 = self.client.post(self.send_url, data=post, files=files, follow=True)

        # 最終的な送信を模擬する追加POST( confirm ステップ)
        resp3 = self.client.post(
            self.send_url,
            data={"send_wizard_view-current_step": "confirm"},
            follow=True,
        )

        # 最終的なレスポンスとリダイレクトを検証
        self.assertIn(resp3.status_code, [200, 302])

        # Message が作成されたことを検証
        last = Message.objects.filter(sender=self.user).order_by("-id").first()
        self.assertIsNotNone(last)
        self.assertEqual(last.title, "Test Confirm")
        self.assertEqual(last.content, "This is a test content for sending.")
