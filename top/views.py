from django.shortcuts import render
from django.contrib import messages


def top_page_view(request):
    if request.user.is_authenticated:
        return render(request, "top/private.html")
    else:
        if "loggedout" in request.GET:
            messages.success(request, "ログアウトが完了しました")
        return render(request, "top/public.html")
