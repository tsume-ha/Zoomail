from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from mail.forms import MessageForm, AttachmentForm, AttachmentFormset
from mail.models import Message, ToGroup
from members.models import User


class FormBoundaryTests(TestCase):
    def setUp(self):
        # テスト用宛先グループ
        self.to_group = ToGroup.objects.create(year=2025, label="2025年度メンバー")

    # 1. MessageForm のバリデーションテスト
    def test_message_form_title_length(self):
        """タイトルの最大文字数を確認"""
        valid_title = "a" * 200
        invalid_title = "a" * 201

        # テスト用ユーザーを作成
        user = User.objects.create_user(email="test@example.com", year=2025)

        # 200文字のタイトル (有効な場合)
        form = MessageForm(
            data={
                "title": valid_title,
                "content": "テスト本文",
                "writer": user.id,  # 適切な`writer`IDを渡す
                "to_groups": [self.to_group.id],  # リスト形式で`to_groups`を渡す
            }
        )
        self.assertTrue(form.is_valid(), "200文字のタイトルは有効であるべき")

        # 201文字のタイトル (無効な場合)
        form = MessageForm(
            data={
                "title": invalid_title,
                "content": "テスト本文",
                "writer": user.id,
                "to_groups": [self.to_group.id],
            }
        )
        self.assertFalse(form.is_valid(), "201文字のタイトルは無効であるべき")

    def test_message_form_content_required(self):
        """本文が空の場合は無効"""
        form = MessageForm(
            data={
                "title": "テストタイトル",
                "content": "",
                "to_groups": [self.to_group.id],
            }
        )
        self.assertFalse(form.is_valid(), "本文が空の場合は無効であるべき")

    def test_message_form_to_groups_required(self):
        """宛先グループが選択されていない場合は無効"""
        form = MessageForm(
            data={"title": "テストタイトル", "content": "テスト本文", "to_groups": []}
        )
        self.assertFalse(
            form.is_valid(), "宛先グループが選択されていない場合は無効であるべき"
        )

    # 2. AttachmentForm のバリデーションテスト
    def test_attachment_form_file_size(self):
        """添付ファイルサイズのテスト"""
        small_file = SimpleUploadedFile("small.txt", b"a" * 2)  # 2バイト
        valid_file = SimpleUploadedFile("valid.txt", b"a" * 3)  # 3バイト
        large_file = SimpleUploadedFile(
            "large.txt", b"a" * (10 * 1024 * 1024 + 1)
        )  # 10MB + 1バイト

        form = AttachmentForm(files={"file": small_file})
        self.assertFalse(form.is_valid(), "2バイトのファイルは無効であるべき")

        form = AttachmentForm(files={"file": valid_file})
        self.assertTrue(form.is_valid(), "3バイトのファイルは有効であるべき")

        form = AttachmentForm(files={"file": large_file})
        self.assertFalse(form.is_valid(), "10MBを超えるファイルは無効であるべき")

    # 3. AttachmentFormset のバリデーションテスト
    def test_attachment_formset_total_size(self):
        """添付ファイルの合計サイズのテスト"""
        file1 = SimpleUploadedFile("file1.txt", b"a" * (10 * 1024 * 1024))  # 10MB
        file2 = SimpleUploadedFile("file2.txt", b"a" * (10 * 1024 * 1024))  # 10MB
        file3 = SimpleUploadedFile("file3.txt", b"a" * (9 * 1024 * 1024))  # 9MB

        formset_data = {
            "form-TOTAL_FORMS": 3,
            "form-INITIAL_FORMS": 0,
            "form-MIN_NUM_FORMS": 0,
        }
        files = {
            "form-0-file": file1,
            "form-1-file": file2,
            "form-2-file": file3,
        }

        formset = AttachmentFormset(data=formset_data, files=files)
        self.assertFalse(formset.is_valid(), "合計29MBのファイルは有効であるべき")

        # 合計30MBを超えた場合
        file4 = SimpleUploadedFile("file4.txt", b"a" * (2 * 1024 * 1024))  # 2MB
        files["form-2-file"] = file4  # これで合計32MB
        formset = AttachmentFormset(data=formset_data, files=files)
        self.assertFalse(formset.is_valid(), "合計30MBを超えるファイルは無効であるべき")
