import tempfile
from datetime import date
from urllib.parse import quote

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse

from kansou.models import Kansouyoushi
from members.models import User


@override_settings(
    MEDIA_ROOT=tempfile.gettempdir(), PRIVATE_STORAGE_ROOT=tempfile.gettempdir()
)
class KansouDownloadTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="kansou-complete@example.com", year=2024
        )
        self.user.fullname = "感想 太郎"
        self.user.furigana = "かんそうたろう"
        self.user.save()

        self.kansou = Kansouyoushi.objects.create(
            title="春ライブ",
            detail="Aチーム",
            performed_at=date(2025, 4, 1),
            created_by=self.user,
            file=SimpleUploadedFile("spring-live.pdf", b"%PDF-1.4 test"),
        )

    def test_index_contains_download_link(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse("kansou:index"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            reverse("kansou:download", kwargs={"kansou_id": self.kansou.id}),
        )

    def test_download_returns_pdf_as_attachment(self):
        self.client.force_login(self.user)

        response = self.client.get(
            reverse("kansou:download", kwargs={"kansou_id": self.kansou.id})
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/pdf")
        self.assertIn("attachment;", response["Content-Disposition"])
        self.assertIn(
            quote("春ライブ (Aチーム).pdf"), response["Content-Disposition"]
        )

    def test_unauthenticated_user_cannot_download(self):
        download_url = reverse("kansou:download", kwargs={"kansou_id": self.kansou.id})

        response = self.client.get(download_url)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response["Location"], f"{settings.LOGIN_URL}?next={download_url}"
        )
