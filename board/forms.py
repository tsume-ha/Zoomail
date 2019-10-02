from django import forms
from django.forms.utils import ErrorList
import datetime
from django.core import validators
from .models import Message
from members.models import User

kaisei = [
(2019,"2019 25期",),
(2018,"2018 24期（会長 : 成基人）",),
(2017,"2017 23期（会長 : 宮武功貴）",),
(2016,"2016 22期（会長 : 木内幹也）",),
(2015,"2015 21期（会長 : 飯干歩）",),
]

validation_error_messages = {
    'no_title': 'タイトルを入力してください',
    'no_year': '宛先を選択してください',
    'no_content': '本文を入力してください',
    'filesize_limit': 'ファイルサイズが30MB以上のため、アップロードできません',
}

def now_kaisei():
    year = datetime.datetime.now().year
    return str(year - 1994) + "期"

def get_user_choice_list():
    return [(str(user.year)+'-'+str(user.pk), user.get_full_name) for user in User.objects.all().order_by('year').order_by('furigana')]

def validate_to(value):
    if value == 'error':
        raise forms.ValidationError(validation_error_messages['no_year'])
    return value

def validate_attachmentfile(value):
    if value.size > 30 * 1024 * 1024: # 30MB
        raise forms.ValidationError(validation_error_messages['filesize_limit'])
    return value

class DivErrorList(ErrorList):
    def __str__(self):
        return self.as_divs()
    def as_divs(self):
        if not self: 
        	return ''
        return '<div class="errorlist">%s</div>' % ''.join(['<div class="error alert alert-danger">%s</div>' % e for e in self])


class SendMessage(forms.Form):
    title = forms.CharField(
        label="件名",
        widget=forms.TextInput(attrs={
            'placeholder': '件名',
            'class': 'form-control',
        }),
        required = True,
        error_messages={'required': validation_error_messages['no_title']}
    )
    year_choice = forms.ChoiceField(# No POSTed DATA is USED in VIEW.PY, This Form is used only for JS
        choices = [(year['year'],year['year']) for year in User.objects.all().order_by('year').reverse().values('year').distinct()],
        widget = forms.Select(attrs={'class': 'form-control'}),
        label = "From"
    )
    written_by = forms.ChoiceField(
        choices = lambda: [(str(user.year).zfill(4)+'-'+str(user.pk), user.get_full_name) for user in User.objects.all().order_by('year').order_by('furigana')],
        label = "送信元",
        widget = forms.Select(attrs={'class': 'form-control'}),
    )
    to = forms.ChoiceField(
        choices = [("error","宛先を選択してください"),(0,"全回メーリス" + "（" + now_kaisei() + "～21期）",)] + kaisei,
        label = "To",
        widget = forms.Select(attrs={'class': 'form-control'}),
        validators = [validate_to],
    )
    content = forms.CharField(
        label="本文",
        widget=forms.Textarea(attrs={
            'placeholder': '本文を入力',
            'class': 'form-control',
        }),
        required = True,
        error_messages={'required': validation_error_messages['no_content']}
    )
    attachmentfile = forms.FileField(
        label = "ファイルを選択してください",
        required = False,
        validators = [validate_attachmentfile],
    )


class Search(forms.Form):
    text = forms.CharField(
        label = "",
        required = False,
        widget = forms.TextInput(attrs = {
            'placeholder': '件名・本文で検索'
        })
    )

class SearchAdvanced(forms.Form):
    title = forms.CharField(
        label = "",
        required = False,
        widget = forms.TextInput(attrs = {
            'placeholder': '件名',
            'class': 'form-control col-5',
        })
    )
    content = forms.CharField(
        label = "",
        required = False,
        widget = forms.TextInput(attrs = {
            'placeholder': '本文',
            'class': 'form-control col-5',
        })
    )
    is_kaisei = forms.BooleanField(
        label = "回生メーリスのみ",
        required = False,
    )
    is_zenkai = forms.BooleanField(
        label = "全回メーリスのみ",
        required = False,
    )
    is_midoku = forms.BooleanField(
        label = "未読メーリスのみ",
        required = False,
    )
    is_marked = forms.BooleanField(
        label = "ブックマークのみ",
        required = False,
    )

class Edit(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['title', 'content']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget = forms.TextInput(attrs={'class': 'form-control',})
        self.fields['content'].widget = forms.Textarea(attrs={'class': 'form-control',})