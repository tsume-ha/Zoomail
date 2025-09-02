from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class LoginRequiredPagesTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Incomplete user: missing fullname or furigana
        cls.incomplete_user = User.objects.create_user(
            email="incomplete@example.com", year=2022
        )
        cls.incomplete_user.fullname = ""
        cls.incomplete_user.furigana = ""
        cls.incomplete_user.save()

        # Complete user: has fullname and furigana
        cls.complete_user = User.objects.create_user(
            email="complete@example.com", year=2023
        )
        cls.complete_user.fullname = "山田太郎"
        cls.complete_user.furigana = "やまだたろう"
        cls.complete_user.save()

        cls.client = Client()

    def test_unauthenticated_redirects_mail_inbox(self):
        url = reverse("mail:inbox")
        resp = self.client.get(url)
        assert resp.status_code in (301, 302)

    def test_unauthenticated_redirects_mail_send(self):
        url = reverse("mail:send")
        resp = self.client.get(url)
        assert resp.status_code in (301, 302)

    def test_unauthenticated_redirects_mail_autocomplete_writer(self):
        url = reverse("mail:send_autocomplete_writer")
        resp = self.client.get(url)
        assert resp.status_code == 403

    def test_incomplete_profile_redirects_mail_inbox(self):
        self.client.force_login(self.incomplete_user)
        url = reverse("mail:inbox")
        resp = self.client.get(url)
        assert resp.status_code in (301, 302)
        target = reverse("members:first_register")
        assert str(resp.get("Location", "")).endswith(target)

    def test_incomplete_profile_redirects_mail_send(self):
        self.client.force_login(self.incomplete_user)
        url = reverse("mail:send")
        resp = self.client.get(url)
        assert resp.status_code in (301, 302)
        target = reverse("members:first_register")
        assert str(resp.get("Location", "")).endswith(target)

    def test_incomplete_profile_redirects_mail_autocomplete_writer(self):
        self.client.force_login(self.incomplete_user)
        url = reverse("mail:send_autocomplete_writer")
        resp = self.client.get(url)
        assert resp.status_code in (301, 302)
        target = reverse("members:first_register")
        assert str(resp.get("Location", "")).endswith(target)

    def test_complete_profile_accesses_get_200(self):
        self.client.force_login(self.complete_user)

        url_inbox = reverse("mail:inbox")
        resp_inbox = self.client.get(url_inbox)
        assert resp_inbox.status_code == 200

        url_send = reverse("mail:send")
        resp_send = self.client.get(url_send)
        assert resp_send.status_code == 200

        url_autocomplete_writer = reverse("mail:send_autocomplete_writer")
        resp_autocomplete_writer = self.client.get(url_autocomplete_writer)
        assert resp_autocomplete_writer.status_code == 200
