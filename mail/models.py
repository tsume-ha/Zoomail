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

# class XMessageID(models.Model):
#     message = models.ForeignKey(User, null=False, on_delete=models.CASCADE, related_name='x_message_id')
#     x_message_id = models.UUIDField(default=uuid.uuid4, editable=False)
#     