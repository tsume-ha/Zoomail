from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class MovieLoginRequiredTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(email="user@example.com", year=2024)
        cls.user.fullname = "Test User"
        cls.user.furigana = "てすとゆーざー"
        cls.user.save()

        cls.client = Client()

    def test_unauthenticated_redirects_movie_index(self):
        url = reverse("movie:index")
        resp = self.client.get(url)
        assert resp.status_code in (301, 302)

    def test_authenticated_access_movie_index(self):
        self.client.force_login(self.user)
        url = reverse("movie:index")
        resp = self.client.get(url)
        assert resp.status_code == 200
