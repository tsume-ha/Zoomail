from django.db import models
from members.models import User
from board.models import Message
import uuid

class SendMailAddress(models.Model):
    user = models.OneToOneField(User, null=False, on_delete=models.CASCADE, related_name='mail_address_user')
    email = models.EmailField(null=False, blank=False, verbose_name="受信用メールアドレス")
    year = models.IntegerField(verbose_name='入部年度')

    def __str__(self):
        return str(self.year) + ' - ' + self.user.get_full_name() +' - ' + self.email

class MessageProcess(models.Model):
    message = models.ForeignKey(Message, null=False, on_delete=models.CASCADE, related_name='x_message_id')
    x_message_id = models.CharField(max_length=100, editable=False)
    email = models.EmailField(null=False, blank=False, verbose_name="送信時メールアドレス")
    Requested = models.BooleanField(default=False, verbose_name="SendGridへ転送")
    Processed = models.BooleanField(default=False, verbose_name="SendGridから送信")
    Delivered = models.BooleanField(default=False, verbose_name="相手サーバーに到達")
    Opened = models.BooleanField(default=False, verbose_name="開封")
    Error_occurd = models.BooleanField(default=False, verbose_name="エラー")
    Error_detail = models.CharField(max_length=100, null=True, blank=True, verbose_name="エラー詳細")

    def __str__(self):
        return self.message.title + ' - Processed:' + str(self.Processed) + ' Delivered:' + str(self.Delivered)
