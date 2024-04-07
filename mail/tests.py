from datetime import datetime
from django.test import TestCase, Client
from django.urls import reverse
from members.models import User
from board.models import Message
from .models import MailLog
from django.conf import settings


class MailStatusViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()

        self.user = User.objects.create_user(email=str(2024) + "mail@gmail.com", year=2024)
        self.user.last_name = "京大"
        self.user.first_name = "太郎"
        self.user.furigana = "きょうだいたろう"
        self.user.save()

        self.message = Message(
            title="Message Example",
            content="Content Example \n" * 10,
            sender=self.user,
            writer=self.user,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        self.message.save()
        self.message.years.create(year=2024)

        self.mail_log = MailLog(
            message=self.message,
            mail_id="test_mail_id",
            email=self.user.email,
            user=self.user,
            send_server=MailLog.SendServerChoices.SES.value,
            status="pending",
            error="",
        )
        self.mail_log.save()

        self.url = "/api/mail/status/"
        self.headers = {"HTTP_X_AUTHORIZATION": settings.MAIL_STATUS_API_KEY}

    def test_get_valid_mail_id(self):
        response = self.client.get(f"{self.url}?message_id={self.mail_log.mail_id}", **self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message_id": self.mail_log.mail_id, "status": self.mail_log.status})

    def test_get_invalid_mail_id(self):
        response = self.client.get(f"{self.url}?message_id=invalid_id", **self.headers)
        self.assertEqual(response.status_code, 400)

    def test_post_valid_data(self):
        data = {"message_id": self.mail_log.mail_id, "status": "delivered", "error_message": "Test error message"}
        response = self.client.post(self.url, data, **self.headers)
        self.assertEqual(response.status_code, 200)
        self.mail_log.refresh_from_db()
        self.assertEqual(response.json(), {"message_id": self.mail_log.mail_id, "status": self.mail_log.status})
        self.assertEqual(self.mail_log.status, "delivered")
        self.assertEqual(self.mail_log.error, "Test error message")

    def test_post_invalid_data(self):
        data = {"message_id": "invalid_id", "status": "delivered", "error_message": "Test error message"}
        response = self.client.post(self.url, data, **self.headers)
        self.assertEqual(response.status_code, 400)

    def test_post_invalid_key(self):
        data = {"mail_id": self.mail_log.mail_id, "status": "delivered", "error_message": "Test error message"}
        response = self.client.post(self.url, data, **self.headers)
        self.assertEqual(response.status_code, 400)
