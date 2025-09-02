from django.test import TestCase
from django.urls import reverse
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from members.models import User
from mail.models import ToGroup, Message


class SendWholeFlowTests(TestCase):
    def setUp(self):
        # テスト用ユーザー作成
        self.user = User.objects.create_user(email="flow@example.com", year=2025)
        self.user.fullname = "Flow Tester"
        self.user.furigana = "ふろー"
        self.user.save()
        self.send_url = reverse("mail:send")

    def test_full_send_wizard_flow(self):
        """
        Compose -> Confirm -> Send の全体フローを通じて Message が作成されることを検証する
        """
        # グループ作成
        group = ToGroup.objects.create(year=2025, label="2025年度メンバー")
        self.client.force_login(self.user)

        # Step 1: Compose 表示を取得
        resp1 = self.client.get(self.send_url)
        wizard = resp1.context["wizard"]
        management_form = wizard["management_form"]
        attachment_formset = resp1.context["attachment_formset"]

        # Step 1 のデータを準備
        post = {"send_wizard_view-current_step": "compose"}
        post.update(
            {
                "writer": str(self.user.id),
                "to_groups": [str(group.id)],
                "title": "Flow Test",
                "content": "Flow content for wizard test.",
            }
        )

        # wizard 管理データを追加
        for field in management_form.hidden_fields():
            post[field.name] = field.value()

        # 添付ファイル用の管理データを追加
        for field in attachment_formset.management_form.hidden_fields():
            post[field.name] = field.value()

        # 添付ファイルを追加
        file_data = SimpleUploadedFile("flow.txt", b"data")
        files = {f"{attachment_formset.prefix}-0-file": file_data}

        # Step 1 -> Step 2 (confirm)
        resp2 = self.client.post(self.send_url, data=post, files=files, follow=True)
        assert resp2.status_code in (200, 302)
        if resp2.status_code == 200:
            self.assertTemplateUsed(resp2, "mail/send_confirm.html")

        # Step 2: Confirm 送信を実行
        resp3 = self.client.post(
            self.send_url,
            data={"send_wizard_view-current_step": "confirm"},
            follow=True,
        )
        assert resp3.status_code in (200, 302)

        # 送信後に Message が作成されていることを検証
        last = Message.objects.filter(sender=self.user).order_by("-id").first()
        self.assertIsNotNone(last)
        self.assertEqual(last.title, "Flow Test")
        self.assertEqual(last.content, "Flow content for wizard test.")
