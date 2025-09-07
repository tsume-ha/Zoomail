from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class TopLoginRequiredTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.incomplete_user = User.objects.create_user(
            email="top_incomplete@example.com", year=2022
        )
        cls.incomplete_user.fullname = ""
        cls.incomplete_user.furigana = ""
        cls.incomplete_user.save()

        cls.complete_user = User.objects.create_user(
            email="top_complete@example.com", year=2023
        )
        cls.complete_user.fullname = "トップ"
        cls.complete_user.furigana = "とっぷ"
        cls.complete_user.save()

        cls.client = Client()

    def test_unauthenticated_view_top_page(self):
        url = reverse("top:top_page")
        resp = self.client.get(url)
        assert resp.status_code == 200

    def test_incomplete_profile_redirects_top_page(self):
        self.client.force_login(self.incomplete_user)
        url = reverse("top:top_page")
        resp = self.client.get(url)
        assert resp.status_code in (301, 302)
        target = reverse("members:first_register")
        assert str(resp.get("Location", "")).endswith(target)

    def test_complete_profile_accesses_top_page(self):
        self.client.force_login(self.complete_user)
        url = reverse("top:top_page")
        resp = self.client.get(url)
        assert resp.status_code == 200
        self.assertTemplateUsed(resp, "top/private.html")
