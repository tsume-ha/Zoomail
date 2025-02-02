from django.db.utils import IntegrityError
from django.core.mail import send_mail

from members.models import User
from social_django.models import UserSocialAuth


class DuplicateGmailAccountError(Exception):
    pass


def Create_Google_User(email, year=0, first_name="", last_name="", furigana=""):
    try:
        user = User.objects.create_user(email, year)
        if first_name != "":
            user.first_name = first_name
        if last_name != "":
            user.last_name = last_name
        if furigana != "":
            user.furigana = furigana
        user.receive_email = email
        user.save()

        content_social = UserSocialAuth(
            user=user,
            provider="google-oauth2",
            uid=email,
        )
        content_social.save()

        subject = "登録が完了しました！【Zoomail】"
        content = user.get_full_name()
        content += "さん"
        content += "\n\n京大アンプラグドのメーリングリスト、Zoomailで、あなたのGoogleアカウント「"
        content += user.email
        content += "」が登録されました。"
        content += "\n\nこれからは、このアカウントを用いてログインすることが出来ます。"
        content += "\n\nサイトへのログインはこちらから\n https://zoomail.ku-unplugged.net"
        content += "\n\nログインできないなどの不具合があった場合は、「info@ku-unplugged.net」まで連絡をお願いします。"
        content += "\n\n京大アンプラグドHP係開発部"

        send_mail(subject, content, "register@zoomail.ku-unplugged.net", [user.email], fail_silently=False)

    except IntegrityError:
        raise DuplicateGmailAccountError("すでに登録されているGoogleアカウントです")
