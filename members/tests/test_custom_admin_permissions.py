from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase
from django.urls import reverse

from members.signals import ADMIN_GROUP_NAME
from photo.models import PhotoAlbum


class CustomAdminStaffPermissionTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.admin_group = Group.objects.create(name=ADMIN_GROUP_NAME)
        photo_album_content_type = ContentType.objects.get_for_model(PhotoAlbum)
        cls.admin_group.permissions.set(
            Permission.objects.filter(content_type=photo_album_content_type)
        )

        cls.staff_user = get_user_model().objects.create_user(
            email="custom-admin-staff@example.com", year=2024
        )
        cls.staff_user.fullname = "管理者"
        cls.staff_user.furigana = "かんりしゃ"
        cls.staff_user.is_staff = True
        cls.staff_user.save()

    def setUp(self):
        self.client.force_login(self.staff_user)

    def test_staff_user_is_added_to_admin_group(self):
        self.assertTrue(self.staff_user.groups.filter(name=ADMIN_GROUP_NAME).exists())

    def test_staff_user_can_access_custom_admin_model_with_group_permissions(self):
        response = self.client.get(reverse("custom_admin:photo_photoalbum_changelist"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "アルバム")

    def test_staff_user_can_add_custom_admin_model_with_group_permissions(self):
        response = self.client.post(
            reverse("custom_admin:photo_photoalbum_add"),
            data={
                "title": "新歓ライブ",
                "url": "https://example.com/album",
                "held_at": "2026-04-01",
            },
        )

        self.assertEqual(response.status_code, 302)
        album = PhotoAlbum.objects.get()
        self.assertEqual(album.title, "新歓ライブ")
        self.assertEqual(album.created_by, self.staff_user)

    def test_user_is_removed_from_admin_group_when_staff_is_removed(self):
        self.staff_user.is_staff = False
        self.staff_user.save()

        self.assertFalse(self.staff_user.groups.filter(name=ADMIN_GROUP_NAME).exists())
