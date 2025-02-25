from django.shortcuts import render, redirect
from .forms import UserUpdateForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages as message


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
            message.success(request, "プロフィールを更新しました")
            return redirect(
                "members:profile"
            )  # リダイレクト先のURL名はプロジェクトに合わせて調整してください
    else:
        form = UserUpdateForm(instance=user)
    return render(request, "members/profile.html", {"form": form})
