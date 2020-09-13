import datetime
import json
import csv

from io import TextIOWrapper
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, To, PlainTextContent
from social_django.models import UserSocialAuth

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.http.response import JsonResponse
from django.conf import settings
from django.core.serializers.json import DjangoJSONEncoder
from django.urls import reverse

from .models import User, TmpMember, TestMail
from .forms import UserUpdateForm, RegisterForm, RegisterCSV
from config.permissions import MemberRegisterPermission, AdminEnterPermission
from board.models import Message, Kidoku
from .create_google_user import DuplicateGmailAccountError
from .create_google_user import Create_Google_User as register


@login_required()
def index(request):
    now_user = request.user
    register_allowed = MemberRegisterPermission(now_user)
    adminenter_allowed = AdminEnterPermission(now_user)
    midoku = (
        Message.objects.filter(Q(years__year=request.user.year) | Q(years__year=0))
        .exclude(kidoku_message__user=now_user)
        .order_by("updated_at")
        .reverse()
    )
    messages_you_send = (
        Message.objects.filter(sender=now_user).order_by("updated_at").reverse()
    )
    messages_you_wrote = (
        Message.objects.filter(writer=now_user)
        .exclude(sender=now_user)
        .order_by("updated_at")
        .reverse()
    )

    if request.method == "POST":
        is_kidoku = request.POST["kidoku"]
        if is_kidoku == "true":
            for message in midoku:
                content = Kidoku(message=message, user=now_user)
                content.save()
    params = {
        "register_allowed": register_allowed,
        "adminenter_allowed": adminenter_allowed,
        "midoku": midoku,
        "yousend": messages_you_send,
        "yourmessage_otherssend": messages_you_wrote,
    }
    return render(request, "members/index.html", params)


@login_required()
def UserUpdate(request):
    now_user = request.user
    form = UserUpdateForm(request.POST or None, instance=now_user)
    if request.method == "POST":
        if form.is_valid():
            content = form.save(commit=False)
            if content.receive_email == "":
                content.receive_email = now_user.email
            content.updated_at = datetime.datetime.now()
            content.save()
            messages.success(request, "更新しました")
            return redirect(to=reverse('members:index'))
        else:
            messages.error(request, "更新できませんでした")
    params = {
        "form": form,
    }
    return render(request, "members/user_update.html", params)


@login_required()
def NewFromLiveLog(request):
    now_user = request.user
    form = UserUpdateForm(request.POST or None, instance=now_user)
    if request.method == "POST":
        if form.is_valid():
            content = form.save(commit=False)
            if content.receive_email == "":
                content.receive_email = now_user.email
            content.updated_at = datetime.datetime.now()
            content.save()
            messages.success(request, "初回登録が完了しました。ようこそ、アンプラ公式メーリスへ！")
            return redirect("/")
        else:
            messages.error(request, "更新できませんでした。入力を確認してください。")
    params = {
        "form": form,
    }
    return render(request, "members/new_from_livelog.html", params)


@login_required()
def UserRegistration(request):
    now_user = request.user
    is_allowed = MemberRegisterPermission(now_user)
    if not is_allowed:
        return redirect(to=reverse('members:index'))
    form = RegisterForm(request.POST or None)
    params = {
        "RegisterForm": form,
    }
    if request.method == "POST":
        if form.is_valid():
            email = request.POST["email"]
            year = request.POST["year"]
            last_name = request.POST["last_name"]
            first_name = request.POST["first_name"]
            furigana = request.POST["furigana"]
            try:
                register(
                    email=email,
                    year=int(year),
                    last_name=last_name,
                    first_name=first_name,
                    furigana=furigana,
                )
                messages.success(request, email + "を登録しました。")
                params["RegisterForm"] = RegisterForm(None)
            except DuplicateGmailAccountError:
                messages.error(request, email + " はすでに登録されているアカウントのため登録できませんでした。")
        else:
            messages.error(request, "登録に失敗しました。入力した値を確かめてください。")
            params["RegisterForm"] = RegisterForm(request.POST)
    return render(request, "members/register.html", params)


# LiveLogに一括登録は任せます。
# （CSV登録はメンテナンス放置します（やる気が...））
@login_required()
def UserRegistrationCSV(request):
    now_user = request.user
    is_allowed = MemberRegisterPermission(now_user)
    if not is_allowed:
        return redirect(to=reverse('members:index'))
    csvform = RegisterCSV(request.POST or None, request.FILES or None)
    params = {
        "RegisterCSV": csvform,
    }
    if request.method == "POST" and csvform.is_valid():
        form_file = request.FILES["csv_file"]
        if not form_file.name.endswith(".csv"):
            messages.error(request, "拡張子がcsvのファイルをアップロードしてください")
            return render(request, "members/registerCSV.html", params)
        form_data = TextIOWrapper(form_file, encoding="utf_8")
        reader = csv.reader(form_data)
        session = request.session.session_key
        try:
            for row in reader:
                if int(row[4]) == 0 or 1990 < int(row[4]) < 2100:
                    try:
                        content = TmpMember(
                            session=session,
                            last_name=row[0],
                            first_name=row[1],
                            furigana=row[2],
                            email=row[3],
                            year=int(row[4]),
                        )
                        content.save()
                    except ValidationError:
                        messages.error(
                            request, ",".join(row) + "の入力情報が正しくないため、以下のリストから外れました。"
                        )
                        continue
                else:
                    messages.error(
                        request, ",".join(row) + "の入部年度情報が正しくないため、以下のリストから外れました。"
                    )
            return redirect("preview/")
        except UnicodeDecodeError:
            messages.error(request, "ファイルのエンコーディングや、正しいCSVファイルか確認ください。")
            return render(request, "members/registerCSV.html", params)
        except ValueError:
            messages.error(request, "ファイルのエンコーディングや、正しいCSVファイルか確認ください。")
            return render(request, "members/registerCSV.html", params)
        except:
            messages.error(
                request, "ファイルのエンコーディングや、正しいCSVファイルか確認ください。直らない場合は、管理者に連絡してください。"
            )
            return render(request, "members/registerCSV.html", params)
        return redirect("preview/")
    return render(request, "members/registerCSV.html", params)


@login_required()
def UserRegistrationPreview(request):
    now_user = request.user
    is_allowed = MemberRegisterPermission(now_user)
    if not is_allowed:
        return redirect(to=reverse('members:index'))
    TmpMembers = TmpMember.objects.filter(session=request.session.session_key).order_by(
        "id"
    )
    params = {"TmpMembers": TmpMembers}
    if request.method == "POST":
        MembersToRegister = TmpMembers
        is_error = False
        for member in MembersToRegister:
            try:
                register(
                    email=member.email,
                    year=member.year,
                    last_name=member.last_name,
                    first_name=member.first_name,
                    furigana=member.furigana,
                )
                member.delete()
            except DuplicateGmailAccountError:
                messages.error(
                    request, member.email + " はすでに登録されているアカウントのため登録できませんでした。"
                )
                is_error = True
        if is_error:
            messages.error(request, "一部ユーザーが登録できませんでした。登録できなかったユーザーが以下の表に残されています。")
            return render(request, "members/register_preview.html", params)
        else:
            messages.success(request, "登録しました")
            return redirect("/mypage/register/csv/")
    return render(request, "members/register_preview.html", params)


@login_required()
def EmailConfirm(request):
    now_user = request.user
    params = {
        "user": now_user,
    }
    if request.method != "POST" or not request.body:
        return render(request, "members/email_confirm.html", params)

    json_dict = json.loads(request.body)
    if json_dict["send"] != "true":
        response = HttpResponse("BAD REQUEST")
        response.status_code = 400
        return response

    now = datetime.datetime.now()
    is_sent_in_5_min = TestMail.objects.filter(
        user=now_user, sent_at__gte=now - datetime.timedelta(minutes=5)
    ).exists()
    if is_sent_in_5_min:
        response = HttpResponse("Rate Limiting")
        response.status_code = 429
        return response

    email = now_user.get_receive_email()
    obj, created = TestMail.objects.update_or_create(
        user=now_user, defaults={"email": email, "sent_at": now}
    )
    text_content = """京大アンプラグド　メーリングリストサービスのUnplugged Messageです。
    このメールはテストメールです。
    このメールが受信できていたら、現在の設定で今後のメーリスが受信できます。

    ---------------
    https://message.ku-unplugged.net/"""
    message = Mail(
        from_email=("zenkai@message.ku-unplugged.net", "テスト用メール"),
        to_emails=[To(email)],
        subject="テストメール【UnpluggedMessage】",
        plain_text_content=PlainTextContent(text_content),
        is_multiple=True,
    )
    if settings.SEND_MAIL:
        sendgrid_client = SendGridAPIClient(settings.SENDGRID_API_KEY)
        response = sendgrid_client.send(message)
        try:
            x_message_id = response.headers["X-Message-Id"]
            obj.x_message_id = x_message_id
            obj.save()
        except Exception:
            return JsonResponse({'error': 'cannot send email'})

    return JsonResponse({'success': 'send mail'})


@login_required()
def getUserInfo(request):
    user = request.user
    return JsonResponse(
        {
            "last_name": user.last_name,
            "first_name": user.first_name,
            "furigana": user.furigana,
            "nickname": user.nickname,
            "email": user.email,
            "receive_email": user.get_receive_email(),
            "send_mail": user.send_mail,
            "year": user.year,
            "created_at": user.created_at,
            "updated_at": user.updated_at,
        }
    )


@login_required()
def OAuthRegisterView(request):
    now_user = request.user
    params = {
        "google": UserSocialAuth.objects.filter(
            user=now_user, provider="google-oauth2"
        ).exists(),
        "livelog": UserSocialAuth.objects.filter(
            user=now_user, provider="auth0"
        ).exists(),
    }
    return render(request, "members/oauth_register.html", params)
