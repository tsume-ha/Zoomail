import tempfile

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse

from members.models import User
from others.models import File


@override_settings(
    MEDIA_ROOT=tempfile.gettempdir(), PRIVATE_STORAGE_ROOT=tempfile.gettempdir()
)
class OthersFileUploadTests(TestCase):
    def setUp(self):
        self.complete_user = User.objects.create_user(
            email="others-complete@example.com", year=2024
        )
        self.complete_user.fullname = "その他ユーザー"
        self.complete_user.furigana = "そのほかゆーざー"
        self.complete_user.save()

        self.incomplete_user = User.objects.create_user(
            email="others-incomplete@example.com", year=2024
        )
        self.incomplete_user.fullname = ""
        self.incomplete_user.furigana = ""
        self.incomplete_user.save()

        self.file_upload_url = reverse("others:file_upload")
        self.file_list_url = reverse("others:file_list")

    def test_file_upload_creates_file_for_complete_user(self):
        self.client.force_login(self.complete_user)

        response = self.client.post(
            self.file_upload_url,
            data={"file": SimpleUploadedFile("sample.txt", b"hello world")},
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(File.objects.count(), 1)
        uploaded = File.objects.first()
        self.assertEqual(uploaded.filename, "sample.txt")
        self.assertEqual(uploaded.created_by, self.complete_user)
        self.assertEqual(uploaded.updated_by, self.complete_user)
        self.assertContains(response, "sample.txt")

    def test_file_upload_requires_file(self):
        self.client.force_login(self.complete_user)

        response = self.client.post(self.file_upload_url, data={})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(File.objects.count(), 0)
        self.assertTrue(response.context["form"].errors)
        self.assertIn("file", response.context["form"].errors)

    def test_incomplete_user_redirected_to_first_register_before_upload(self):
        self.client.force_login(self.incomplete_user)

        response = self.client.get(self.file_upload_url)

        self.assertIn(response.status_code, (301, 302))
        self.assertTrue(
            str(response.get("Location", "")).endswith(
                reverse("members:first_register")
            )
        )

    def test_deleted_file_is_not_displayed_in_file_list(self):
        visible = File.objects.create(
            filename="visible.txt", created_by=self.complete_user
        )
        visible.file = SimpleUploadedFile("visible.txt", b"abc")
        visible.save()
        hidden = File.objects.create(
            filename="hidden.txt", created_by=self.complete_user, is_deleted=True
        )
        hidden.file = SimpleUploadedFile("hidden.txt", b"abc")
        hidden.save()

        self.client.force_login(self.complete_user)
        response = self.client.get(self.file_list_url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "visible.txt")
        self.assertNotContains(response, "hidden.txt")

    def test_delete_action_sets_logical_delete_flag(self):
        file_obj = File.objects.create(
            filename="delete-target.txt", created_by=self.complete_user
        )
        file_obj.file = SimpleUploadedFile("delete-target.txt", b"abc")
        file_obj.save()

        self.client.force_login(self.complete_user)
        response = self.client.post(
            reverse("others:file_edit", kwargs={"pk": file_obj.pk}),
            data={"delete": "on", "filename": "delete-target", "file": file_obj.file},
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        file_obj.refresh_from_db()
        self.assertTrue(file_obj.is_deleted)
        self.assertFalse(response.context["files"].filter(pk=file_obj.pk).exists())
