from django import forms
from django.core import validators

from members.models import User


class FirstRegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'last_name',
            'first_name',
            'furigana',
            'nickname',
            'receive_email',
            'send_mail'
            ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"
        self.fields['receive_email'].required = False
        self.fields['nickname'].required = False
        self.fields['send_mail'].widget.attrs['class'] = 'mx-2'
        self.fields['last_name'].widget.attrs['placeholder'] = '京大'
        self.fields['first_name'].widget.attrs['placeholder'] = '太郎'
        self.fields['furigana'].widget.attrs['placeholder'] = 'きょうだいたろう'
        self.fields['nickname'].widget.attrs['placeholder'] = 'たろー'

    def get_object(self):
        return self.request.user
