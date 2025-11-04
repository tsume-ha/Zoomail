from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class KansouLoginRequiredTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Incomplete user: missing fullname or furigana
        cls.incomplete_user = User.objects.create_user(
            email="kun_incomplete@example.com", year=2022
        )
        cls.incomplete_user.fullname = ""
        cls.incomplete_user.furigana = ""
        cls.incomplete_user.save()

        # Complete user: has fullname and furigana
        cls.complete_user = User.objects.create_user(
            email="kun_complete@example.com", year=2023
        )
        cls.complete_user.fullname = "完了カンソウ"
        cls.complete_user.furigana = "かんそう"
        cls.complete_user.save()

        cls.client = Client()

    def test_unauthenticated_redirects_index(self):
        url = reverse("kansou:index")
        resp = self.client.get(url)
        assert resp.status_code in (301, 302)

    def test_incomplete_profile_redirects_index(self):
        self.client.force_login(self.incomplete_user)
        url = reverse("kansou:index")
        resp = self.client.get(url)
        assert resp.status_code in (301, 302)
        target = reverse("members:first_register")
        assert str(resp.get("Location", "")).endswith(target)

    def test_complete_profile_accesses_index(self):
        self.client.force_login(self.complete_user)
        url = reverse("kansou:index")
        resp = self.client.get(url)
        assert resp.status_code == 200
