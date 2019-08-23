from django import forms
from django.core import validators
from .models import Kansouyoushi
import datetime


class KansouUploadForm(forms.Form):
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


    live = forms.ChoiceField(
        choices = livename,
        label = "ライブ名",
        widget = forms.Select(attrs={'class': 'form-control'}),
        required = True,
        )

    # title = forms.CharField(
    #     label = "ライブ名",
    #     required = True,
    #     widget = forms.TextInput(
    #         attrs = {'class': 'form-control',
    #                  'placeholder': 'ライブ名'}
    #         )
    #     )
    detail = forms.CharField(
        label = "追加事項",
        required = False,
        widget = forms.TextInput(
            attrs = {'class': 'form-control',
                     'placeholder': '例）1回生の分です。'}
            )
        )
    numbering = forms.IntegerField(
        label="ナンバリング",
        required = False,
        widget = forms.NumberInput(
            attrs = {'class': 'form-control',}
            )
        )

    file = forms.FileField(
        label="PDFファイル",
        required =True,
        # widget = forms.FileInput(
        #     attrs = {'class': 'form-control',}
        #     )
        )

    performed_at = forms.DateField(
        label = "ライブ日",
        required = True,
        initial = datetime.date.today(),
        widget = forms.DateInput(attrs={'type': 'date',
                                        'class': 'form-control',})
        )
