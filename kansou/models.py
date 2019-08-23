from django.db import models
from members.models import User
from private_storage.fields import PrivateFileField

class Kansouyoushi(models.Model):
    title = models.CharField(max_length=200)
    detail = models.CharField(max_length=200, blank=True)
    live = models.IntegerField()
    numbering = models.IntegerField(default=1)
    file = PrivateFileField(upload_to='kansoyoshi/%Y', null=True) # filename = '2019_6_22_newlive_1.pdf'
    performed_at = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='kansou_creater')
    def __str__(self):
        return self.message.title

    livename = (#            index     名称
        'other',#            0          その他
        'sinkanlive'#        1          新歓
        'freshmanlive',#     2          新人
        'junelive',#         3          6月
        'septemberlive',#    4          9月
        'octoberlive',#      5          10月
        'christmaslive',#    6          クリスマス
        'newyearlive',#      7          あけおめ
        'marchlive',#        8          3月

    )