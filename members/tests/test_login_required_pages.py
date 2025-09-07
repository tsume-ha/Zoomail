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

    def test_unauthenticated_redirects_members_index(self):
        url = reverse("members:index")
        resp = self.client.get(url)
        assert resp.status_code in (301, 302)

    def test_unauthenticated_redirects_members_first_register(self):
        url = reverse("members:first_register")
        resp = self.client.get(url)
        assert resp.status_code in (301, 302)

    def test_unauthenticated_redirects_members_profile(self):
        url = reverse("members:profile")
        resp = self.client.get(url)
        assert resp.status_code in (301, 302)

    def test_unauthenticated_redirects_members_test_mail(self):
        url = reverse("members:test_mail")
        resp = self.client.get(url)
        assert resp.status_code in (301, 302)

    def test_unauthenticated_redirects_members_invitation_list(self):
        url = reverse("members:invitation_list")
        resp = self.client.get(url)
        assert resp.status_code in (301, 302)

    def test_unauthenticated_redirects_members_edit_invitation(self):
        url = reverse("members:edit_invitation", args=[1])
        resp = self.client.get(url)
        assert resp.status_code in (301, 302)

    def test_unauthenticated_redirects_members_delete_invitation(self):
        url = reverse("members:delete_invitation", args=[1])
        resp = self.client.get(url)
        assert resp.status_code in (301, 302)
