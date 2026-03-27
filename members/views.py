from datetime import datetime, timedelta
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404

from mail.send import MailContent, MailRecipient, SympleMailSender
from .models import TestMail, UserInvitation
from .forms import UserUpdateForm, TestMailForm, UserInvitationForm, FirstRegisterForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages as django_messages


@login_required
def index(request):
    return render(request, "members/index.html")


@login_required
def first_register(request):
    if request.user and request.user.is_filled_vaild():
        django_messages.info(
            request,
            "すでに初回登録は完了しています。",
        )
        return redirect("members:profile")
    if request.method == "POST":
        form = FirstRegisterForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            django_messages.success(
                request, "初回登録が完了しました。ようこそZoomailへ！"
            )
            return redirect("members:index")
        else:
            if not request.POST.get("receive_email", "").strip():
                form.fields["receive_email"].widget.attrs["value"] = request.user.email
    else:
        form = FirstRegisterForm(
            instance=request.user, initial={"receive_email": request.user.email}
        )
        django_messages.success(
            request,
            "LiveLogとの連携が完了しました！続けてZoomailにて必要な情報を登録してください。",
        )
    return render(request, "members/first_register.html", {"form": form})


@login_required
def profile(request):
    user = request.user  # ログイン中のユーザー情報を取得
    if request.method == "POST":
        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            django_messages.success(request, "プロフィールを更新しました")
            print(form.changed_data)
            if "send_mail" in form.changed_data:
                if form.cleaned_data["send_mail"]:
                    django_messages.info(
                        request, "現在の設定：メーリスが配信されます。"
                    )
                else:
                    django_messages.warning(
                        request, "現在の設定ではメーリスは配信されません。"
                    )
            return redirect(
                "members:profile"
            )  # リダイレクト先のURL名はプロジェクトに合わせて調整してください
    else:
        form = UserUpdateForm(instance=user)
    return render(
        request,
        "members/profile.html",
        {
            "form": form,
            "livelog_login": user.livelog_login,
            "google_login": user.google_login,
        },
    )


@login_required
def test_mail(request):
    user = request.user
    receive_email = (
        user.get_receive_email()
    )  # Assuming user model has receive_email field

    can_send = not TestMail.objects.filter(
        user=user, sent_at__gte=datetime.now() - timedelta(minutes=5)
    ).exists()

    if request.method == "POST":
        form = TestMailForm(request.POST)
        if form.is_valid() and form.cleaned_data.get("send") and can_send:
            # Send test email
            mail_content = MailContent(
                subject="メーリス受信テスト",
                text=f"{user.fullname or user.username} 様\n\nこれはメーリス受信テストメールです。\nこのメールが正常に届いていれば、メーリスの受信設定は正常です。",
            )
            recipient = MailRecipient(
                to_email=receive_email,
                from_email="zenkai@zoomail.ku-unplugged.net",
                from_name="Zoomail テスト配信",
                user=user,
            )

            try:
                sender = SympleMailSender()
                sender.set_content(mail_content)
                sender.set_recipient_list([recipient])
                sender.send()
                TestMail.objects.create(
                    user=user,
                    email=receive_email,
                    sent_at=datetime.now(),
                    x_message_id="dummy",
                )
                django_messages.success(
                    request,
                    f"テストメールを送信しました。 「zenkai@zoomail.ku-unplugged.net」から届いているメールを確認してください。",
                )
            except Exception as e:
                django_messages.error(request, f"メール送信エラー: {str(e)}")

            return redirect("mypage:test_mail")
        elif not can_send:
            django_messages.warning(
                request,
                "テストメールは5分に1回のみ送信できます。しばらくお待ちください。",
            )
    else:
        form = TestMailForm()

    context = {
        "form": form,
        "receive_email": receive_email,
        "can_send": can_send,
    }
    return render(request, "members/test_mail.html", context)


@login_required
def invitation_list(request):
    if not request.user.is_staff:
        return HttpResponseForbidden("権限がありません")

    """View for displaying the list of invitations and the invitation form"""
    invitations = UserInvitation.objects.filter(inviter=request.user)

    if request.method == "POST":
        form = UserInvitationForm(request.POST)
        if form.is_valid():
            invitation = form.save(commit=False)
            invitation.inviter = request.user
            invitation.save()

            mail_content = MailContent(
                subject="京大アンプラグド Zoomail へ招待されました",
                text=(
                    "こんにちは！\n"
                    "京大アンプラグド メーリングリスト配信サービスの Zoomail です。\n\n"
                    f"このメールアドレスは、{request.user.fullname or request.user.email} 様によりZoomailへ招待されました。\n\n"
                    "アクセスするには以下のリンクから 「Googleアカウント」 を選択してログインしてください。\n\n"
                    f"https://zoomail.ku-unplugged.net/\n\n\n"
                    "このメールは Zoomail より自動送信されました。心当たりのない場合は破棄してください。"
                ),
            )
            recipient = MailRecipient(
                to_email=invitation.email,
                from_email="invitation@zoomail.ku-unplugged.net",
                from_name="京大アンプラグド Zoomail",
                user=None,
            )

            try:
                sender = SympleMailSender()
                sender.set_content(mail_content)
                sender.set_recipient_list([recipient])
                sender.send()
                django_messages.success(
                    request, f"「{invitation.email}」宛に招待メールを送信しました。"
                )
            except Exception as e:
                django_messages.error(request, f"メール送信エラー: {str(e)}")

            return redirect("members:invitation_list")
    else:
        form = UserInvitationForm()

    context = {
        "invitations": invitations,
        "form": form,
    }
    return render(request, "members/invitation_list.html", context)


@login_required
def edit_invitation(request, invitation_id):
    """View for editing an existing invitation"""
    if not request.user.is_staff:
        return HttpResponseForbidden("権限がありません")

    invitation = get_object_or_404(
        UserInvitation, id=invitation_id, inviter=request.user
    )

    if request.method == "POST":
        form = UserInvitationForm(request.POST, instance=invitation)
        if form.is_valid():
            form.save()

            # # Send updated invitation email
            # subject = "サークルサイト招待情報の更新"
            # message = (
            #     f"{invitation.fullname} 様\n\n"
            #     f"あなたへの招待情報が{request.user.fullname or request.user.email}によって更新されました。\n"
            #     f"下記のリンクからアカウントを作成してください。\n\n"
            #     f"{settings.BASE_URL}/register/?email={invitation.email}"
            # )
            # from_email = settings.DEFAULT_FROM_EMAIL
            # recipient_list = [invitation.email]

            try:
                # send_mail(subject, message, from_email, recipient_list)
                django_messages.success(
                    request, f"{invitation.email}に更新通知メールを送信しました。"
                )
            except Exception as e:
                django_messages.error(request, f"メール送信エラー: {str(e)}")

            django_messages.success(request, "招待情報を更新しました。")

    context = {
        "form": form,
        "invitation": invitation,
    }
    return render(request, "members/edit_invitation.html", context)


@login_required
def delete_invitation(request, invitation_id):
    """View for editing an existing invitation"""
    if not request.user.is_staff:
        return HttpResponseForbidden("権限がありません")

    invitation = get_object_or_404(
        UserInvitation, id=invitation_id, inviter=request.user
    )
    django_messages.success(request, f"{invitation.email}の招待を取り消しました。")

    return redirect("members:invitation_list")
