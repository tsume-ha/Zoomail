from django.db import models
from members.models import User
from private_storage.fields import PrivateFileField


# To Do
# live をChoiceFieldに
# upload_toでファイル名を指定してしまう


class Kansouyoushi(models.Model):
    title = models.CharField(max_length=200, verbose_name="ライブ名")
    detail = models.CharField(max_length=200, blank=True, verbose_name="その他特記事項")
    file = PrivateFileField(upload_to="kansoyoshi/%Y/", null=True, verbose_name="PDFファイル")
    performed_at = models.DateField(verbose_name="ライブ日")
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name="kansou_creater")

    def __str__(self):
        return self.performed_at.strftime("%Y-%m-%d") + " : " + self.title

    # livename = [
    #     ('sinkanlive','新歓ライブ'),
    #     ('junelive','6月ライブ'),
    #     ('freshmanlive','新人ライブ'),
    #     ('septemberlive','9月ライブ'),
    #     ('octoberlive','10月ライブ'),
    #     ('christmaslive','クリスマスライブ'),
    #     ('newyearlive','あけおめライブ'),
    #     ('marchlive','3月ライブ'),
    #     ('other','その他'),
    # ]
