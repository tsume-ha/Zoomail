from django import forms
from django.forms.utils import ErrorList
import datetime
from django.core import validators
from django.template.defaultfilters import filesizeformat

kaisei = [
(2019,"2019 25期",),
(2018,"2018 24期（会長 : 成基人）",),
(2017,"2017 23期（会長 : 宮武功貴）",),
(2016,"2016 22期（会長 : 木内幹也）",),
(2015,"2015 21期（会長 : 飯干歩）",),
]

def now_kaisei():
    year = datetime.datetime.now().year
    return str(year - 1994) + "期"

def validate_to(value):
    if value == 'error':
        raise forms.ValidationError('エラー : 宛先を選択してください')
    return value


class DivErrorList(ErrorList):
    def __str__(self):
        return self.as_divs()
    def as_divs(self):
        if not self: 
        	return ''
        return '<div class="errorlist">%s</div>' % ''.join(['<div class="error alert alert-danger">%s</div>' % e for e in self])


class SendMessage(forms.Form):
    title = forms.CharField(label="件名",widget=forms.TextInput(attrs={
        'placeholder': '件名',
        'class': 'form-control',
        }))
    to = forms.ChoiceField(
        choices = [("error","宛先を選択してください"),(0,"全回メーリス" + "（" + now_kaisei() + "～21期）",)] + kaisei,
        label = "宛先",
        widget = forms.Select(attrs={'class': 'form-control'}),
        validators = [validate_to],
    )
    content = forms.CharField(label="本文",widget=forms.Textarea(attrs={
        'placeholder': '本文を入力',
        'class': 'form-control',
    }))



def validate_attachmentfile(value):
    if value.size > 30 * 1024 * 1024: # 30MB
        raise forms.ValidationError('ファイルサイズが30MB以上のため、アップロードできません')
    return value

class Attachment(forms.Form):
    attachmentfile = forms.FileField(
        label = "ファイルを選択してください",
        required = False,
        validators = [validate_attachmentfile],
    )
        
        
class Search(forms.Form):
    text = forms.CharField(label="",required=False,widget=forms.TextInput(attrs={
        'placeholder': '件名・本文で検索'
        }))