from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from mail.models import Attachment, Message, ToGroup
from members.models import User


class AttachmentDownloadTests(TestCase):
    def setUp(self):
        self.user_2025 = User.objects.create_user(
            email="attach2025@example.com", year=2025
        )
        self.user_2025.fullname = "Attach 2025"
        self.user_2025.furigana = "てすと"
        self.user_2025.save()

        self.user_2024 = User.objects.create_user(
            email="attach2024@example.com", year=2024
        )
        self.user_2024.fullname = "Attach 2024"
        self.user_2024.furigana = "てすと"
        self.user_2024.save()

        self.group_2025 = ToGroup.objects.create(year=2025, label="2025年度メンバー")
        self.group_all = ToGroup.objects.create(year=0, label="全体メーリス")

        self.message_2025 = Message.objects.create(
            title="2025添付",
            content="2025本文",
            sender=self.user_2025,
            writer=self.user_2025,
        )
        self.message_2025.to_groups.add(self.group_2025)
        self.attachment_2025 = Attachment.objects.create(
            message=self.message_2025,
            file=SimpleUploadedFile("year2025.txt", b"abc"),
            org_filename="year2025.txt",
        )

        self.message_all = Message.objects.create(
            title="全体添付",
            content="全体本文",
            sender=self.user_2025,
            writer=self.user_2025,
        )
        self.message_all.to_groups.add(self.group_all)
        self.attachment_all = Attachment.objects.create(
            message=self.message_all,
            file=SimpleUploadedFile("all.txt", b"abc"),
            org_filename="all.txt",
        )

    def test_attachment_download_allowed_for_same_year_user(self):
        self.client.force_login(self.user_2025)

        response = self.client.get(
            reverse(
                "mail:attachment_download",
                kwargs={
                    "message_id": self.message_2025.id,
                    "attachment_id": self.attachment_2025.id,
                },
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("year2025.txt", response.headers.get("Content-Disposition", ""))

    def test_attachment_download_allowed_for_global_message(self):
        self.client.force_login(self.user_2024)

        response = self.client.get(
            reverse(
                "mail:attachment_download",
                kwargs={
                    "message_id": self.message_all.id,
                    "attachment_id": self.attachment_all.id,
                },
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("all.txt", response.headers.get("Content-Disposition", ""))

    def test_attachment_download_denied_for_other_year_user(self):
        self.client.force_login(self.user_2024)

        response = self.client.get(
            reverse(
                "mail:attachment_download",
                kwargs={
                    "message_id": self.message_2025.id,
                    "attachment_id": self.attachment_2025.id,
                },
            )
        )

        self.assertEqual(response.status_code, 404)

    def test_attachment_download_returns_404_when_attachment_not_belong_to_message(
        self,
    ):
        self.client.force_login(self.user_2025)

        response = self.client.get(
            reverse(
                "mail:attachment_download",
                kwargs={
                    "message_id": self.message_2025.id,
                    "attachment_id": self.attachment_all.id,
                },
            )
        )

        self.assertEqual(response.status_code, 404)
