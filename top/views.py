from django.shortcuts import render
from django.contrib import messages


def top_page_view(request):
    if not request.user.is_authenticated:
        if "loggedout" in request.GET:
            messages.success(request, "ログアウトが完了しました")
        return render(request, "top/public.html")
    else:
        return render(request, "top/private.html")
