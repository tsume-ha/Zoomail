from django.db import models
from members.models import User
from private_storage.fields import PrivateFileField

class Kansouyoushi(models.Model):
    live = models.CharField(max_length=200)
    detail = models.CharField(max_length=200, blank=True)
    numbering = models.IntegerField(default=1)
    file = PrivateFileField(upload_to='kansoyoshi/', null=True) # filename = '2019_6_22_newlive_1.pdf'
    performed_at = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='kansou_creater')
    def __str__(self):
        return self.performed_at.strftime('%Y-%m-%d') + ' : ' + self.live

    livename = (#            index     名称
        'other',#            0          その他
        'sinkanlive'#        1          新歓
        'junelive',#         2          6月
        'freshmanlive',#     3          新人
        'septemberlive',#    4          9月
        'octoberlive',#      5          10月
        'christmaslive',#    6          クリスマス
        'newyearlive',#      7          あけおめ
        'marchlive',#        8          3月

    )