import datetime
import json
from django.contrib.messages.api import success
from django.forms.widgets import EmailInput

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, To, PlainTextContent
from social_django.models import UserSocialAuth

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.http.response import JsonResponse
from django.db.utils import IntegrityError

from django.conf import settings
from .models import User, TestMail
from .forms import UserUpdateForm, MailSettingsForm, RegisterForm, MailTestForm, GoogleUnlinkForm
from config.permissions import MemberRegisterPermission, AdminEnterPermission
from .create_google_user import DuplicateGmailAccountError
from .create_google_user import Create_Google_User as register


@login_required()
def mailTestAPI(request):
    user = request.user
    if request.method != "POST":
        messages.warning(request, "無効なリクエストです")
        return userInfo(request, status_code=400)

    form = MailTestForm(request.POST)

    if not form.is_valid():
        messages.error(request, "フォームが無効で、送信されませんでした")
        return userInfo(request, status_code=400)

    # 5分に1回しか送れない制限
    now = datetime.datetime.now()
    is_sent_in_5_min = TestMail.objects.filter(user=user, sent_at__gte=now - datetime.timedelta(minutes=5)).exists()
    if is_sent_in_5_min:
        messages.error(request, "テストメールを送信できるのは5分に1回です。時間をおいてもう一度お試しください。")
        response = HttpResponse("Rate Limiting")
        response.status_code = 429
        return response

    # sendrifで送信
    email = user.get_receive_email()
    obj, _ = TestMail.objects.update_or_create(user=user, defaults={"email": email, "sent_at": now})
    text_content = """京大アンプラグド　メーリングリストサービスのUnplugged Messageです。
    このメールはテストメールです。
    このメールが受信できていたら、現在の設定で今後のメーリスが受信できます。

    ---------------
    https://message.ku-unplugged.net/"""
    # message = Mail(
    #     from_email=("zenkai@message.ku-unplugged.net", "テスト用メール"),
    #     to_emails=[To(email)],
    #     subject="テストメール【UnpluggedMessage】",
    #     plain_text_content=PlainTextContent(text_content),
    #     is_multiple=True,
    # )
    # if settings.SEND_MAIL:
    #     sendgrid_client = SendGridAPIClient(settings.SENDGRID_API_KEY)
    #     response = sendgrid_client.send(message)
    #     try:
    #         x_message_id = response.headers["X-Message-Id"]
    #         obj.x_message_id = x_message_id
    #         obj.save()
    #     except Exception:
    #         response = HttpResponse("Send mail faild")
    #         response.status_code = 500
    #         return response

    response = HttpResponse("Test mail was sent.")
    response.status_code = 200
    return response


@login_required()
def userInfo(request, status_code=200):
    import time

    time.sleep(3)
    user = request.user
    return JsonResponse(
        {
            "userInfo": {
                "id": user.id,
                "lastName": user.last_name,
                "firstName": user.first_name,
                "furigana": user.furigana,
                "nickname": user.nickname,
                "shortname": user.get_short_name(),
                "email": user.email,
                "receiveEmail": user.get_receive_email(),
                "livelogEmail": user.livelog_email,
                "sendMail": user.send_mail,
                "year": user.year,
                "createdAt": user.created_at,
                "updatedAt": user.updated_at,
                "googleOauth2": UserSocialAuth.objects.filter(user=user, provider="google-oauth2").exists(),
                "livelogAuth0": UserSocialAuth.objects.filter(user=user, provider="auth0").exists(),
                "isSuperuser": user.is_superuser,
                "isStaff": user.is_staff,
                "canRegisterUser": MemberRegisterPermission(user),
            }
        },
        status=status_code,
    )


@login_required()
def googleOauthUnlink(request):
    user = request.user
    if request.method != "POST":
        messages.warning(request, "無効なリクエストです")
        return userInfo(request, status_code=400)

    form = GoogleUnlinkForm(request.POST)
    if not form.is_valid():
        messages.error(request, "解除できませんでした。開発者にお問い合わせください。")
        for field_name in form._errors:
            messages.error(request, field_name + form._errors[field_name].as_text())
        return userInfo(request, status_code=400)

    if UserSocialAuth.objects.filter(user=user, provider="auth0").exists() and user.livelog_email:
        query = UserSocialAuth.objects.filter(user=user, provider="google-oauth2")
        assert query.count() < 3
        # 一応安全確認 なんかのバグで全件取得とかできてしまったら怖い
        query.delete()
        try:
            user.email = user.livelog_email
            user.save()
            messages.success(request, "Googleアカウントの紐づけを解除しました。")
            return userInfo(request)
        except IntegrityError:
            messages.error(request, "Googleアカウントでのログインは無効化されましたが、データを全て削除できませんでした。")
            return userInfo(request, status_code=500)

    return userInfo(request, status_code=400)


@login_required()
def profile(request):
    user = request.user
    if request.method != "POST":
        messages.warning(request, "無効なリクエストです")
        return userInfo(request, status_code=400)

    initial = {
        "last_name": user.last_name,
        "first_name": user.first_name,
        "furigana": user.furigana,
        "nickname": user.nickname,
    }
    form = UserUpdateForm(request.POST, instance=user, initial=initial)

    if not form.is_valid():
        messages.error(request, "更新できませんでした")
        for field_name in form._errors:
            messages.error(request, field_name + form._errors[field_name].as_text())
        return userInfo(request, status_code=400)

    elif form.has_changed():
        content = form.save(commit=False)
        content.updated_at = datetime.datetime.now()
        content.save()
        messages.success(request, "更新しました")

    else:
        messages.info(request, "更新はありませんでした")

    return userInfo(request)


@login_required()
def mailSettingsAPI(request):
    user = request.user
    if request.method != "POST":
        messages.warning(request, "無効なリクエストです")
        return userInfo(request, status_code=400)

    initial = {"receive_email": user.receive_email, "send_mail": user.send_mail}
    form = MailSettingsForm(request.POST, instance=user, initial=initial)

    if not form.is_valid():
        messages.error(request, "更新できませんでした")
        for field_name in form._errors:
            messages.error(request, field_name + form._errors[field_name].as_text())
        return userInfo(request, status_code=400)

    elif form.has_changed():
        content = form.save(commit=False)
        content.updated_at = datetime.datetime.now()
        content.save()
        messages.success(request, "更新しました")

    else:
        messages.info(request, "更新はありませんでした")

    return userInfo(request)


@login_required()
def registerAPI(request):
    now_user = request.user
    is_allowed = MemberRegisterPermission(now_user)
    if not is_allowed:
        raise PermissionError

    if request.method != "POST":
        messages.error(request, "不正なリクエストです")
        response = HttpResponse("BAD REQUEST")
        response.status_code = 400
        return response

    form = RegisterForm(request.POST)
    if form.is_valid():
        form.save()
        # save()でメール送信が走る
        messages.success(request, "登録しました。")
        return JsonResponse({"success": True})

    else:
        messages.error(request, form.errors.as_text())

    messages.error(request, "入力されたデータが不正です。")
    messages.error(request, "登録に失敗しました。")
    return JsonResponse({"success": False})
