from django.shortcuts import render
from django.contrib import messages

from .models import content_log, Announcement


def top_page_view(request):
    if request.user.is_authenticated:
        new_contents = content_log(LIST_NUM=5)
        announcements = Announcement.objects.order_by("-created_at")[:3]
        context = {"new_contents": new_contents, "announcements": announcements}
        return render(request, "top/private.html", context)
    else:
        if "loggedout" in request.GET:
            messages.success(request, "ログアウトが完了しました")
        return render(request, "top/public.html")
