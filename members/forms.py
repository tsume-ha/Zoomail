import datetime

from django import forms
from django.core import validators
from django.conf import settings

from social_django.models import UserSocialAuth
from utils.mail import SympleMessageSendClient
from .models import User, TestMail


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["last_name", "first_name", "furigana", "nickname"]


class MailSettingsForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["receive_email", "send_mail"]


class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["email", "year", "last_name", "first_name", "furigana"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["furigana"].validators = [
            validators.RegexValidator(
                regex="^[ぁ-んー]+$",
                message="ふりがなは全角ひらがなのみで入力してください。",
            )
        ]

    def clean_year(self):
        year = self.cleaned_data["year"]
        if not (year == 0 or 1990 < year < 2100):
            raise forms.ValidationError("無効な入部年度です。第24期などでなく、入部年度（2018）を入力してください。")
        return year

    def clean_email(self):
        email = self.cleaned_data["email"]
        if UserSocialAuth.objects.filter(uid=email).exists():
            raise forms.ValidationError("このGoogleアカウントはすでに登録されています")
        return email

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=commit)
        user.receive_email = self.cleaned_data["email"]
        user.social_auth.create(provider="google-oauth2", uid=self.cleaned_data["email"])
        user.save()

        # send a mail
        sendgridclient = SympleMessageSendClient(
            title="招待されました！【Zoomail】京大アンプラグド",
            text="ようこそ、京大アンプラグドへ！{}さん\n\n"
            "京大アンプラグドのメーリスシステム「Zoomail」に招待されました\n"
            "ログインするには、以下のURLからZoomailのウェブサイトへ行き、\n"
            "「Googleでログイン」ボタンからこのGmailのアカウントでログインしてください。\n\n"
            "【ログインURL】\n"
            "https://zoomail.ku-unplugged.net \n\n"
            "ログインできないなど、なにかお困りの時は info@ku-unplugged.net までご連絡ください。\n"
            "京大アンプラグドHP係開発部".format(user.get_full_name()),
            to_email=user.email,
            from_email="register@zoomail.ku-unplugged.net",
        )
        if settings.SEND_MAIL:
            sendgridclient.send()

        return user


class MailTestForm(forms.ModelForm):
    def __init__(self, data, user):
        super().__init__(data)
        self.__user = user

    class Meta:
        model = TestMail
        fields = []

    send = forms.BooleanField(required=True)

    def clean_send(self):
        bool = self.cleaned_data["send"]
        if not bool:
            raise forms.ValidationError("リクエストの形式が無効です")
        return bool

    def clean(self):
        super().clean()
        if TestMail.objects.filter(
            user=self.__user, sent_at__gte=(datetime.datetime.now() - datetime.timedelta(minutes=5))
        ).exists():
            raise forms.ValidationError("テストメールを送信できるのは5分に1回です。時間をおいてもう一度お試しください。")

    def save(self):
        # send a mail
        sendgridclient = SympleMessageSendClient(
            title="テストメールです【Zoomail】",
            text="このメールは、Zoomailからの送信テストメールです\n\n"
            "このメールが受信できていたら、現在の設定で今後のメーリスが受信できます。ご安心ください。\n"
            "これからも京大アンプラグドをよろしくお願いします。\n"
            "-------------\n"
            "Zoomail - 京大アンプラグドの部内メール配信サービス\n"
            "https://zoomail.ku-unplugged.net/ \n\n"
            "京大アンプラグド HP係",
            to_email=self.__user.get_receive_email(),
            from_email="zenkai@zoomail.ku-unplugged.net",
        )
        if settings.SEND_MAIL:
            response = sendgridclient.send()
            x_message_id = response.headers["X-Message-Id"]
        else:
            x_message_id = "settings.SEND_EMAIL was False"
        content = super().save(commit=False)
        content.sent_at = datetime.datetime.now()
        content.user = self.__user
        content.email = self.__user.get_receive_email()
        content.x_message_id = x_message_id
        content.save()
        return content


class GoogleUnlinkForm(forms.Form):
    unlink = forms.BooleanField(required=True)

    def clean_send(self):
        bool = self.cleaned_data["unlink"]
        if not bool:
            raise forms.ValidationError("リクエストの形式が無効です")
        return bool
