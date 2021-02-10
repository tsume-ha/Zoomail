from django import forms
from django.core import validators

from .models import User


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['last_name', 'first_name', 'furigana', 'nickname']


class MailSettingsForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['receive_email', 'send_mail']


class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'year', 'last_name', 'first_name', 'furigana']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['furigana'].validators = [validators.RegexValidator(
            regex=u'^[ぁ-んー]+$',
            message='ふりがなは全角ひらがなのみで入力してください。',
        )]

    def clean_year(self):
        year = self.cleaned_data['year']
        if not ( year == 0 or 1990 < year < 2100 ):
            raise forms.ValidationError('無効な入部年度です。第24期などでなく、入部年度（2018）を入力してください。')
        return year


