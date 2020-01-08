from django.db import models
from members.models import User
from private_storage.fields import PrivateFileField

class Kansouyoushi(models.Model):
    live = models.CharField(max_length=200, verbose_name='ライブ名')
    detail = models.CharField(max_length=200, blank=True, verbose_name='その他特記事項')
    numbering = models.IntegerField(default=1, verbose_name='ナンバリング')
    file = PrivateFileField(upload_to='kansoyoshi/%Y/', null=True, verbose_name='PDFファイル')
    performed_at = models.DateField(verbose_name='ライブ日')
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='kansou_creater')
    def __str__(self):
        return self.performed_at.strftime('%Y-%m-%d') + ' : ' + self.live

    livename = [
        ('sinkanlive','新歓ライブ'),
        ('junelive','6月ライブ'),
        ('freshmanlive','新人ライブ'),
        ('septemberlive','9月ライブ'),
        ('octoberlive','10月ライブ'),
        ('christmaslive','クリスマスライブ'),
        ('newyearlive','あけおめライブ'),
        ('marchlive','3月ライブ'),
        ('other','その他'),
    ]

    def translate_livename(self):
        for l_name in self.livename:
            if l_name[0] == self.live:
                return l_name[1]
        return '（ライブ名不明）'#見つからなかった場合にこれを返す
        