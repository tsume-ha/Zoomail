from django.db import models
from members.models import User
from board.models import Message
import uuid


class SendMailAddress(models.Model):
    user = models.OneToOneField(User, null=False, on_delete=models.CASCADE, related_name="mail_address_user")
    email = models.EmailField(null=False, blank=False, verbose_name="受信用メールアドレス")
    year = models.IntegerField(verbose_name="入部年度")

    def __str__(self):
        return str(self.year) + " - " + self.user.get_full_name() + " - " + self.email


class MessageProcess(models.Model):
    message = models.ForeignKey(Message, null=True, on_delete=models.CASCADE, related_name="process")
    x_message_id = models.CharField(max_length=100, editable=False, null=True, blank=True)
    email = models.EmailField(null=False, blank=False, verbose_name="送信時メールアドレス")
    Requested = models.BooleanField(default=False, verbose_name="SendGridへ転送")
    Processed = models.BooleanField(default=False, verbose_name="SendGridから送信")
    Delivered = models.BooleanField(default=False, verbose_name="相手サーバーに到達")
    Opened = models.BooleanField(default=False, verbose_name="開封")
    Error_occurd = models.BooleanField(default=False, verbose_name="エラー")
    Error_detail = models.CharField(max_length=1000, null=True, blank=True, verbose_name="エラー詳細")

    def __str__(self):
        if self.message is not None:
            return (
                str(self.message.title) + " - Processed:" + str(self.Processed) + " Delivered:" + str(self.Delivered)
            )
        else:
            return str(self.message) + " - Processed:" + str(self.Processed) + " Delivered:" + str(self.Delivered)

class MailLog(models.Model):

    class SendServerChoices(models.IntegerChoices):
        SENDGRID = 1
        SES = 2

    message = models.ForeignKey(Message, null=True, on_delete=models.CASCADE, related_name="logs")
    mail_id = models.CharField(max_length=100, editable=False, null=True, blank=True)
    email = models.EmailField(null=False, blank=False, verbose_name="送信時メールアドレス")
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name="mail_logs")
    send_server = models.PositiveSmallIntegerField(null=True, blank=True, choices=SendServerChoices.choices)
    status = models.CharField(max_length=20, null=True, blank=True)
    error = models.CharField(max_length=1000, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
