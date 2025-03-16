from django import forms
from .models import User, UserInvitation


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


class UserInvitationForm(forms.ModelForm):
    class Meta:
        model = UserInvitation
        fields = [
            "email",
            "year",
        ]
        widgets = {
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "year": forms.NumberInput(
                attrs={"class": "form-control", "min": "2000", "max": "2100"}
            ),
        }
        help_texts = {
            "year": "2024年4月入部の場合、2024を入力してください。",
        }

    def clean_year(self):
        year = self.cleaned_data.get("year")
        if year < 1980 or year > 2100:
            raise forms.ValidationError(
                "入部年度は30期などの数字ではなく、西暦4桁で入力してください。"
            )
        return year
