from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class FirstRegisterFlowTest(TestCase):
    def test_full_flow_redirect_and_register_and_index(self):
        # Step 0: create an incomplete user (furigana/fullname empty)
        incomplete_user = User.objects.create_user(
            email="incomplete@example.com", year=2022
        )
        incomplete_user.fullname = ""
        incomplete_user.furigana = ""
        incomplete_user.save()

        client = Client()
        client.force_login(incomplete_user)

        # Step 1: access index -> should redirect to first_register due to incomplete profile
        url_index = reverse("members:index")
        resp = client.get(url_index)
        self.assertIn(resp.status_code, (301, 302))
        url_first_register = reverse("members:first_register")
        self.assertTrue(str(resp.get("Location", "")).endswith(url_first_register))

        # Step 2: GET first_register form
        resp = client.get(url_first_register)
        self.assertEqual(resp.status_code, 200)
        self.assertIn("form", resp.context)

        # Step 3: submit the first_register form with required fields
        post_data = {
            "fullname": "山田太郎",
            "furigana": "やまだたろう",
            "receive_email": "incomplete@example.com",
        }
        resp = client.post(url_first_register, data=post_data)
        self.assertIn(resp.status_code, (301, 302))
        # After successful registration, should redirect to index
        self.assertTrue(str(resp.get("Location", "")).endswith(url_index))

        # Step 4: verify User model has been updated
        user_refreshed = User.objects.get(id=incomplete_user.id)
        self.assertEqual(user_refreshed.fullname, "山田太郎")
        self.assertEqual(user_refreshed.furigana, "やまだたろう")

        # Step 5: access index again -> should be accessible now
        resp = client.get(url_index)
        self.assertEqual(resp.status_code, 200)

    def test_first_register_fails_when_fullname_missing(self):
        user = User.objects.create_user(email="missing-fullname@example.com", year=2022)
        user.fullname = ""
        user.furigana = ""
        user.save()

        client = Client()
        client.force_login(user)
        url = reverse("members:first_register")

        resp = client.post(
            url,
            data={
                "fullname": "",
                "furigana": "やまだたろう",
                "receive_email": "missing-fullname@example.com",
                "send_mail": "on",
            },
        )

        self.assertEqual(resp.status_code, 200)
        self.assertIn("form", resp.context)
        self.assertIn("fullname", resp.context["form"].errors)
        user.refresh_from_db()
        self.assertEqual(user.fullname, "")

    def test_first_register_fails_when_furigana_missing(self):
        user = User.objects.create_user(email="missing-furigana@example.com", year=2022)
        user.fullname = ""
        user.furigana = ""
        user.save()

        client = Client()
        client.force_login(user)
        url = reverse("members:first_register")

        resp = client.post(
            url,
            data={
                "fullname": "山田太郎",
                "furigana": "",
                "receive_email": "missing-furigana@example.com",
                "send_mail": "on",
            },
        )

        self.assertEqual(resp.status_code, 200)
        self.assertIn("form", resp.context)
        self.assertIn("furigana", resp.context["form"].errors)
        user.refresh_from_db()
        self.assertEqual(user.furigana, "")

    def test_first_register_completed_user_redirects_to_profile(self):
        user = User.objects.create_user(email="completed@example.com", year=2022)
        user.fullname = "完了ユーザー"
        user.furigana = "かんりょうゆーざー"
        user.save()

        client = Client()
        client.force_login(user)
        url = reverse("members:first_register")

        resp = client.get(url)

        self.assertIn(resp.status_code, (301, 302))
        self.assertTrue(
            str(resp.get("Location", "")).endswith(reverse("members:profile"))
        )
