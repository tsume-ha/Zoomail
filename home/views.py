import datetime
from django.http.response import JsonResponse, HttpResponse

from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect


from .models import Announcement, NewContent
from .forms import FirstRegisterForm


def index(request):
    if not request.user.is_authenticated:
        if "loggedout" in request.GET:
            messages.success(request, "ログアウトが完了しました")
        return render(request, "public.html")
    else:
        return render(request, "private.html")


def login(request):
    params = {}
    if "next" in request.GET:
        params["next"] = request.GET["next"]
    return render(request, "admin/login.html", params)


@login_required()
def tempUser(request):
    return JsonResponse(
        {
            "email": request.user.email if request.user.email else "",
            "lastName": request.user.last_name if request.user.last_name else "",
            "firstName": request.user.first_name if request.user.first_name else "",
            "furigana": request.user.furigana if request.user.furigana else "",
            "nickname": request.user.nickname if request.user.nickname else "",
        }
    )


@login_required()
def firstRegister(request):
    return render(request, "first_register.html")


@login_required()
def firstRegisterAPI(request):
    if not request.method == "POST":
        return HttpResponse("Bad request", status=400)
    form = FirstRegisterForm(request.POST or None, instance=request.user)
    if form.is_valid():
        content = form.save(commit=False)
        if content.receive_email == "":
            content.receive_email = request.user.email
        content.updated_at = datetime.datetime.now()
        content.save()
        messages.success(request, "初回登録が完了しました。ようこそ、アンプラ公式メーリスへ！")
        return HttpResponse("OK")
    else:
        return HttpResponse(form.errors.as_json(), status=400)


@login_required()
def homeAPI(request):
    announcements = Announcement.objects.order_by("-created_at")[:5]
    newcontents = NewContent.objects.order_by("index")[:5]
    return JsonResponse(
        {
            "newContents": [
                {"id": newcontent.id, "genre": newcontent.genre, "title": newcontent.title, "path": newcontent.path}
                for newcontent in newcontents
            ],
            "announcements": [
                {
                    "id": announcement.id,
                    "date": announcement.created_at.strftime("%Y/%m/%d"),
                    "text": announcement.text,
                }
                for announcement in announcements
            ],
        }
    )
