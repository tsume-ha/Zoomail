from django.shortcuts import render
from django.contrib import messages


def top_page_view(request):
    if request.user.is_authenticated:
        new_contents = [
            "An item",
            "A second item",
            "A third item",
            "A fourth item",
            "And a fifth one",
        ]
        announcements = [
            "Announcement 1",
            "Announcement 2",
            "Announcement 3",
            "Announcement 4",
            "Announcement 5",
        ]
        context = {"new_contents": new_contents, "announcements": announcements}
        return render(request, "top/private.html", context)
    else:
        if "loggedout" in request.GET:
            messages.success(request, "ログアウトが完了しました")
        return render(request, "top/public.html")
