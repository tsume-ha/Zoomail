import os
import datetime
import uuid
from django.db import models
from members.models import User
from private_storage.fields import PrivateFileField
from django.utils import timezone


class ToGroup(models.Model):
    class Meta:
        verbose_name = "宛先グループ"
        verbose_name_plural = "宛先グループ"

    year = models.PositiveSmallIntegerField(null=False, blank=False)
    leader = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="to_kaichou",
        verbose_name="会長",
    )
    label = models.CharField(
        max_length=40,
        null=True,
        blank=True,
        help_text="ここに表示名(ex「全回メーリス」)を指定すると、選択肢としてこの表示名が表示されます。指定がなければ「2018 24期」のように表示されます。",
        verbose_name="表示名",
    )

    def __str__(self):
        return self.text()

    def text(self):
        if self.year == 0:
            return self.label
        if 1995 < self.year < 2100:
            if self.label:
                return self.label
            if self.leader:
                return "{} {}期（会長：{}）".format(
                    self.year, self.year - 1994, self.leader.get_short_name()
                )
            if not self.leader:
                return "{} {}期".format(self.year, self.year - 1994)
        else:
            return str(self.year)


class Message(models.Model):
    class Meta:
        verbose_name = "メーリス"
        verbose_name_plural = "メーリス"

    title = models.CharField(max_length=200)
    content = models.TextField()
    sender = models.ForeignKey(
        User, null=True, on_delete=models.SET_NULL, related_name="send_message"
    )
    # 転載時に使用。
    # 文章を書いた人がwriter、アップロードした人がsender。
    # 通常なら sender == writer で同じになる。
    writer = models.ForeignKey(
        User, null=True, on_delete=models.SET_NULL, related_name="write_message"
    )
    to_groups = models.ManyToManyField(ToGroup, related_name="messages")
    updated_at = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "mes_ID=" + str(self.id) + ", title=" + self.title


def custom_upload_to(instance, filename):
    extension = os.path.splitext(filename)[-1]
    unique_filename = f"attachments/{uuid.uuid4()}{extension}"
    return unique_filename


class Attachment(models.Model):
    message = models.ForeignKey(
        Message, null=True, on_delete=models.CASCADE, related_name="attachments"
    )
    file = PrivateFileField(
        upload_to=custom_upload_to,
        max_file_size=10 * 1000 * 1000,  # < 10*1024*1024, 余裕を持たせる
        null=True,
        blank=True,
    )
    org_filename = models.CharField(max_length=200, null=False, blank=False)

    def __str__(self):
        return self.org_filename

    def extension(self):
        _, extension = os.path.splitext(self.file.name)
        return extension

    def is_image(self):
        ImageExtensions = [".gif", ".png", ".jpeg", ".jpg", ".bmp"]
        return self.extension() in [str.lower() for str in ImageExtensions] + [
            str.upper() for str in ImageExtensions
        ]


class MailLog(models.Model):

    class SendServerChoices(models.IntegerChoices):
        SENDGRID = 1
        SES = 2

    class StatusChoices(models.TextChoices):
        PENDING = "pending"
        SUCCESS = "success"
        FAILED = "failed"

    message = models.ForeignKey(
        Message, null=True, on_delete=models.CASCADE, related_name="logs"
    )
    mail_id = models.CharField(max_length=100, editable=False, null=True, blank=True)
    email = models.EmailField(
        null=False, blank=False, verbose_name="送信時メールアドレス"
    )
    user = models.ForeignKey(
        User, null=True, on_delete=models.CASCADE, related_name="mail_logs"
    )
    send_server = models.PositiveSmallIntegerField(
        null=True, blank=True, choices=SendServerChoices.choices
    )
    status = models.CharField(max_length=20, null=True, blank=True)
    error = models.CharField(max_length=1000, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
