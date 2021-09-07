import datetime
from django.http.response import JsonResponse

from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect


from .models import ContentLog, Announcement
from .forms import FirstRegisterForm

def index(request):
    if not request.user.is_authenticated:
        if 'loggedout' in request.GET:
            messages.success(request, "ログアウトが完了しました")
        return render(request, 'public.html')
    else:
        return render(request, 'SPA.html')


def login(request):
    params = {
    
    }
    if 'next' in request.GET:
        params['next'] = request.GET['next'] 
    return render(request, 'admin/login.html', params)


@login_required()
def firstRegister(request):
    now_user = request.user
    form = FirstRegisterForm(request.POST or None, instance=now_user)
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
    return render(request, "home/first_register.html", params)


@login_required()
def homeAPI(request):
    messages.success(request, "メッセージを送信できる")
    messages.success(request, "メッセージを送信できる2")
    messages.success(request, "メッセージを送信できる3")
    announcements = Announcement.objects.order_by('-created_at')[:5]
    return JsonResponse({
        'content_log': [
            {
                "genre": i[1],
                "title": i[3],
                "url": i[4]
            } for i in ContentLog(LIST_NUM=5)
        ],
        'announcements': [
            {
                "date": announcement.created_at.strftime("%Y/%m/%d"),
                "text": announcement.text
            } for announcement in announcements
        ]

    })