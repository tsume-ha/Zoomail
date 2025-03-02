from django import forms
from .models import User


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["receive_email", "send_mail", "fullname", "nickname", "furigana"]
        widgets = {
            "receive_email": forms.EmailInput(attrs={"class": "form-control"}),
            "send_mail": forms.CheckboxInput(
                attrs={"class": "form-check-input", "role": "switch"}
            ),
            "fullname": forms.TextInput(attrs={"class": "form-control"}),
            "nickname": forms.TextInput(attrs={"class": "form-control"}),
            "furigana": forms.TextInput(attrs={"class": "form-control"}),
        }
        labels = {
            "receive_email": "受信用メールアドレス",
            "send_mail": "メーリスを受信する",
            "fullname": "フルネーム",
            "nickname": "ニックネーム",
            "furigana": "ふりがな",
        }


class TestMailForm(forms.Form):
    send = forms.BooleanField(required=False)
