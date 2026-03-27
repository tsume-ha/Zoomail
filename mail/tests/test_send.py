from django.test import TestCase
from django.urls import reverse
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from unittest.mock import Mock, patch
from members.models import User
from mail.models import MailLog, ToGroup, Message
from mail.send import MailContent, MailRecipient, SympleMailSender, MailisSender


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


class SenderPayloadTests(TestCase):
    def test_simple_mail_sender_posts_content_and_recipients_payload(self):
        sender = SympleMailSender()
        sender.set_content(MailContent(subject="件名", text="本文"))
        sender.set_recipient_list(
            [
                MailRecipient(
                    to_email="to@example.com",
                    from_email="from@example.com",
                    from_name="差出人",
                )
            ]
        )

        mock_response = Mock()
        mock_response.raise_for_status = Mock()

        with patch("mail.send.requests.post", return_value=mock_response) as mock_post:
            sender._request()

        _, kwargs = mock_post.call_args
        self.assertEqual(kwargs["json"]["content"], {"subject": "件名", "text": "本文"})
        self.assertEqual(len(kwargs["json"]["recipients"]), 1)
        self.assertEqual(kwargs["json"]["recipients"][0]["to"], "to@example.com")
        self.assertEqual(
            kwargs["json"]["recipients"][0]["from"],
            {"email": "from@example.com", "name": "差出人"},
        )
        self.assertEqual(kwargs["json"]["attachments"], [])

    def test_mailis_sender_builds_recipient_specific_from_addresses(self):
        writer = User.objects.create_user(email="writer@example.com", year=2025)
        writer.fullname = "送信者 テスト"
        writer.furigana = "そうしんしゃ"
        writer.save()

        user_zenkai = User.objects.create_user(email="all@example.com", year=2024)
        user_zenkai.receive_email = "all-receive@example.com"
        user_zenkai.send_mail = True
        user_zenkai.save()

        user_kaisei = User.objects.create_user(email="year@example.com", year=2025)
        user_kaisei.receive_email = "year-receive@example.com"
        user_kaisei.send_mail = True
        user_kaisei.save()

        zenkai_group = ToGroup.objects.create(year=0, label="全回")
        kaisei_group = ToGroup.objects.create(year=2025, label="2025")

        message = Message.objects.create(
            title="件名",
            content="本文",
            sender=writer,
            writer=writer,
        )
        message.to_groups.set([zenkai_group, kaisei_group])

        sender = MailisSender(message=message)

        recipients_by_email = {
            recipient.to_email: recipient for recipient in sender.recipient_list
        }
        self.assertIn("all-receive@example.com", recipients_by_email)
        self.assertEqual(
            recipients_by_email["all-receive@example.com"].from_email,
            "zenkai@zoomail.ku-unplugged.net",
        )
        self.assertIn("year-receive@example.com", recipients_by_email)
        self.assertEqual(
            recipients_by_email["year-receive@example.com"].from_email,
            "2025kaisei@zoomail.ku-unplugged.net",
        )

    def test_send_creates_logs_per_recipient(self):
        sender = SympleMailSender()
        sender.set_content(MailContent(subject="件名", text="本文"))
        sender.set_recipient_list(
            [
                MailRecipient(
                    to_email="to1@example.com",
                    from_email="from@example.com",
                    from_name="差出人1",
                ),
                MailRecipient(
                    to_email="to2@example.com",
                    from_email="from@example.com",
                    from_name="差出人2",
                ),
            ]
        )

        mock_response = Mock()
        mock_response.raise_for_status = Mock()

        with patch("mail.send.requests.post", return_value=mock_response), patch(
            "mail.send.SEND_MAIL", True
        ):
            count = sender.send()

        self.assertEqual(count, 2)
        self.assertEqual(MailLog.objects.count(), 2)
