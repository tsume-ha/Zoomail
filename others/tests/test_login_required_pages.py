from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class OthersLoginRequiredTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Incomplete user: missing fullname or furigana
        cls.incomplete_user = User.objects.create_user(
            email="other_incomplete@example.com", year=2022
        )
        cls.incomplete_user.fullname = ""
        cls.incomplete_user.furigana = ""
        cls.incomplete_user.save()

        # Complete user: has fullname and furigana
        cls.complete_user = User.objects.create_user(
            email="other_complete@example.com", year=2023
        )
        cls.complete_user.fullname = "その他"
        cls.complete_user.furigana = "そのほか"
        cls.complete_user.save()

        cls.client = Client()

    def _resolve_index_url(self):
        try:
            return reverse("others:file_list")
        except Exception:
            return "/others/"

    def test_unauthenticated_redirects_index(self):
        url = self._resolve_index_url()
        resp = self.client.get(url)
        self.assertIn(resp.status_code, (301, 302))

    def test_incomplete_profile_redirects_index(self):
        self.client.force_login(self.incomplete_user)
        url = self._resolve_index_url()
        resp = self.client.get(url)
        self.assertIn(resp.status_code, (301, 302))
        target = reverse("members:first_register")
        self.assertTrue(str(resp.get("Location", "")).endswith(target))

    def test_complete_profile_accesses_index(self):
        self.client.force_login(self.complete_user)
        url = self._resolve_index_url()
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    # New tests for additional endpoints
    def test_unauthenticated_redirects_file_upload(self):
        url = reverse("others:file_upload")
        resp = self.client.get(url)
        self.assertIn(resp.status_code, (301, 302))

    def test_incomplete_profile_redirects_file_upload(self):
        self.client.force_login(self.incomplete_user)
        url = reverse("others:file_upload")
        resp = self.client.get(url)
        self.assertIn(resp.status_code, (301, 302))
        target = reverse("members:first_register")
        self.assertTrue(str(resp.get("Location", "")).endswith(target))

    def test_complete_profile_accesses_file_upload(self):
        self.client.force_login(self.complete_user)
        url = reverse("others:file_upload")
        resp = self.client.get(url)
        self.assertIn(resp.status_code, (200,))
