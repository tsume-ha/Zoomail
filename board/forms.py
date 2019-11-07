from django import forms
from django.core import validators
from .models import Message, Attachment

kaisei = [
(2019,"2019 25期",),
(2018,"2018 24期（会長 : 成基進）",),
(2017,"2017 23期（会長 : 宮武功貴）",),
(2016,"2016 22期（会長 : 木内幹也）",),
(2015,"2015 21期（会長 : 飯干歩）",),
(2014,"2014 20期（会長 : 緒方悠介）",),
]

validation_error_messages = {
    'no_title': 'タイトルを入力してください',
    'no_year': '宛先を選択してください',
    'no_content': '本文を入力してください',
    'no_writer': '送信者を確定してください',
    'filesize_limit': 'ファイルサイズが30MB以上のため、アップロードできません',
}

def validate_attachmentfile(value):
    if value.size > 30 * 1024 * 1024: # 30MB
        raise forms.ValidationError(validation_error_messages['filesize_limit'])
    return value

class SendMessage(forms.Form):
    title = forms.CharField(
        label="件名",
        widget=forms.TextInput(attrs={
            'placeholder': '件名',
        }),
        required = True,
        error_messages={'required': validation_error_messages['no_title']}
    )
    year_choice = forms.ChoiceField(# No POSTed DATA is USED in VIEW.PY, This Form is used only for JS
        label = "From",
        required = False,
    )
    written_by = forms.ChoiceField(
        label = "送信元",
        error_messages={'required': validation_error_messages['no_writer']}
    )
    to = forms.MultipleChoiceField(
        choices = [(0,"全回メーリス")] + kaisei,
        label = "To",
    )
    content = forms.CharField(
        label="本文",
        widget=forms.Textarea(attrs={
            'placeholder': '本文を入力',
        }),
        required = True,
        error_messages={'required': validation_error_messages['no_content']}
    )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"

AttachmentFileFormset = forms.inlineformset_factory(
    Message, Attachment, fields=('attachment_file',),
    extra=3, max_num=6, can_delete=False
)
        


class SearchAdvanced(forms.Form):
    text = forms.CharField(
        label = "",
    )
    is_kaisei = forms.BooleanField(
        label = "回生メーリスのみ",
    )
    is_zenkai = forms.BooleanField(
        label = "全回メーリスのみ",
    )
    is_midoku = forms.BooleanField(
        label = "未読メーリスのみ",
    )
    is_marked = forms.BooleanField(
        label = "ブックマークのみ",
    )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = False
            field.widget.attrs["class"] = "toggle"
        self.fields['text'].widget = forms.TextInput(attrs={
            'placeholder': '件名・本文で検索',
            'class': 'form-control formtext',
            })



class Edit(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['title', 'content']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget = forms.TextInput(attrs={'class': 'form-control',})
        self.fields['content'].widget = forms.Textarea(attrs={'class': 'form-control',})