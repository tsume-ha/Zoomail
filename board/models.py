import os
import datetime
from django.db import models
from members.models import User
from private_storage.fields import PrivateFileField
from django.utils import timezone


class Message(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()

    sender = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name="send_message")
    # 転載時に使用。
    # 文章を書いた人がwriter、アップロードした人がsender。
    # 通常なら sender == writer で同じになる。
    writer = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name="write_message")

    updated_at = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "mes_ID=" + str(self.id) + ", title=" + self.title


class MessageYear(models.Model):
    year = models.IntegerField()
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name="years")

    ALL = 0

    def display(self):
        if self.year == self.ALL:
            return "全回"

        return self.year

    def __str__(self):
        return str(self.display())


def custom_upload_to(instance, filename):
    now = datetime.datetime.now()
    path = "document/" + now.strftime("%Y/%m/%d/") + now.strftime("%Y_%m_%d__%H_%M_%S")
    extension = os.path.splitext(filename)[-1]
    return path + extension


class Attachment(models.Model):
    message = models.ForeignKey(Message, null=True, on_delete=models.CASCADE, related_name="attachments")
    attachment_file = PrivateFileField(
        upload_to=custom_upload_to, max_file_size=10 * 1000 * 1000, null=True, blank=True  # < 10*1024*1024
    )

    def __str__(self):
        return self.message.title

    def extension(self):
        _, extension = os.path.splitext(self.attachment_file.name)
        return extension

    def isImage(self):
        ImageExtensions = [".gif", ".png", ".jpeg", ".jpg", ".bmp"]
        return self.extension() in [str.lower() for str in ImageExtensions] + [str.upper() for str in ImageExtensions]

    def fileName(self):
        _, fileName = os.path.split(self.attachment_file.name)
        return fileName


class Tag(models.Model):
    name = models.CharField(max_length=30)
    messages = models.ManyToManyField(Message)

    def __str__(self):
        return self.name


class Bookmark(models.Model):
    message = models.ForeignKey(Message, null=False, on_delete=models.CASCADE, related_name="bookmark_message")
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE, related_name="bookmark_user")

    def __str__(self):
        return self.user.get_full_name() + " - " + self.message.title


class ToGroup(models.Model):
    class Meta:
        verbose_name = "宛先グループ"
        verbose_name_plural = "宛先グループ"
    year = models.PositiveSmallIntegerField(null=False, blank=False)
    leader = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name="to_kaichou", verbose_name="会長")
    label = models.CharField(
        max_length=40,
        null=True,
        blank=True,
        help_text="ここに表示名(ex「全回メーリス」)を指定すると、選択肢としてこの表示名が表示されます。指定がなければ「2018 24期」のように表示されます。",
        verbose_name="表示名"
    )

    def __str__(self):
        return self.text()

    def text(self):
        if self.year == 0:
            return self.label
        if 2000 < self.year < 2100:
            if self.label:
                return self.label
            if self.leader:
                return "{} {}期（会長：{}）".format(self.year, self.year - 1994, self.leader.get_full_name())
            if not self.leader:
                return "{} {}期".format(self.year, self.year - 1994)
        else:
            return str(self.year)
