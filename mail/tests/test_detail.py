from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from mail.models import Attachment, Message, ToGroup
from members.models import User


class MailDetailViewTests(TestCase):
    def setUp(self):
        self.user_2025 = User.objects.create_user(
            email="detail2025@example.com", year=2025
        )
        self.user_2025.fullname = "2025 User"
        self.user_2025.furigana = "てすと"
        self.user_2025.save()

        self.user_2024 = User.objects.create_user(
            email="detail2024@example.com", year=2024
        )
        self.user_2024.fullname = "2024 User"
        self.user_2024.furigana = "てすと"
        self.user_2024.save()

        self.writer_user = User.objects.create_user(
            email="writer@example.com", year=2023
        )
        self.writer_user.fullname = "Writer User"
        self.writer_user.furigana = "てすと"
        self.writer_user.save()

        self.group_2025 = ToGroup.objects.create(year=2025, label="2025年度メンバー")
        self.group_2024 = ToGroup.objects.create(year=2024, label="2024年度メンバー")
        self.group_all = ToGroup.objects.create(year=0, label="全体メーリス")

        self.message_2025 = Message.objects.create(
            title="2025向け詳細",
            content="2025本文",
            sender=self.user_2025,
            writer=self.user_2025,
        )
        self.message_2025.to_groups.add(self.group_2025)

        self.message_all = Message.objects.create(
            title="全体向け詳細",
            content="全体本文",
            sender=self.user_2025,
            writer=self.user_2025,
        )
        self.message_all.to_groups.add(self.group_all)

        self.sender_visible_message = Message.objects.create(
            title="senderなら見える",
            content="sender本文",
            sender=self.user_2025,
            writer=self.user_2024,
        )
        self.sender_visible_message.to_groups.add(self.group_2024)

        self.writer_visible_message = Message.objects.create(
            title="writerなら見える",
            content="writer本文",
            sender=self.user_2024,
            writer=self.writer_user,
        )
        self.writer_visible_message.to_groups.add(self.group_2024)

        self.attachment_message = Message.objects.create(
            title="添付あり詳細",
            content="添付本文",
            sender=self.user_2025,
            writer=self.user_2025,
        )
        self.attachment_message.to_groups.add(self.group_2025)
        Attachment.objects.create(
            message=self.attachment_message,
            file=SimpleUploadedFile("detail.txt", b"abc"),
            org_filename="detail.txt",
        )

    def test_detail_accessible_for_target_year_user(self):
        self.client.force_login(self.user_2025)
        response = self.client.get(
            reverse("mail:detail", kwargs={"id": self.message_2025.id})
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "2025向け詳細")
        self.assertContains(response, "2025本文")

    def test_detail_not_accessible_for_other_year_user(self):
        self.client.force_login(self.user_2024)
        response = self.client.get(
            reverse("mail:detail", kwargs={"id": self.message_2025.id})
        )

        self.assertEqual(response.status_code, 404)

    def test_detail_accessible_for_all_group_message(self):
        self.client.force_login(self.user_2024)
        response = self.client.get(
            reverse("mail:detail", kwargs={"id": self.message_all.id})
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "全体向け詳細")

    def test_detail_accessible_for_sender_even_if_group_year_differs(self):
        self.client.force_login(self.user_2025)
        response = self.client.get(
            reverse("mail:detail", kwargs={"id": self.sender_visible_message.id})
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "senderなら見える")

    def test_detail_accessible_for_writer_even_if_group_year_differs(self):
        self.client.force_login(self.writer_user)
        response = self.client.get(
            reverse("mail:detail", kwargs={"id": self.writer_visible_message.id})
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "writerなら見える")

    def test_detail_displays_sender_and_attachment(self):
        self.client.force_login(self.user_2025)
        response = self.client.get(
            reverse("mail:detail", kwargs={"id": self.attachment_message.id})
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user_2025.get_short_name())
        self.assertContains(response, "detail.txt")
