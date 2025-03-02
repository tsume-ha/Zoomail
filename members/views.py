from datetime import datetime, timezone
from django.shortcuts import render, redirect
from .forms import UserUpdateForm, TestMailForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages as django_messages


@login_required
def index(request):
    return render(request, "members/index.html")


@login_required
def profile(request):
    user = request.user  # ログイン中のユーザー情報を取得
    if request.method == "POST":
        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            django_messages.success(request, "プロフィールを更新しました")
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
    receive_email = user.receive_email  # Assuming user model has receive_email field

    # Get the last test email time from session
    last_test_email_time = request.session.get("last_test_email_time", None)
    can_send = True

    if last_test_email_time:
        # Convert from string to datetime
        last_time = datetime.fromisoformat(last_test_email_time)
        # Check if it's been at least 5 minutes
        time_diff = datetime.now() - last_time
        if time_diff.total_seconds() < 300:  # 5 minutes in seconds
            can_send = False

    if request.method == "POST":
        form = TestMailForm(request.POST)
        if form.is_valid() and form.cleaned_data.get("send") and can_send:
            # Send test email
            subject = "メーリス受信テスト"
            message = f"{user.fullname or user.username} 様\n\nこれはメーリス受信テストメールです。\nこのメールが正常に届いていれば、メーリスの受信設定は正常です。"
            from_email = "zenkai@zoomail.ku-unplugged.net"
            recipient_list = [receive_email]

            try:
                # send_mail(subject, message, from_email, recipient_list)
                # mesdjango_messagessage.success(
                #     request,
                #     "テストメールを送信しました。メールボックスを確認してください。",
                # )
                # Update the last test email time
                request.session["last_test_email_time"] = datetime.now().isoformat()
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
