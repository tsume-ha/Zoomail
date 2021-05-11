import datetime

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.contrib.auth import logout
from django.conf import settings
from urllib.parse import urlencode
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

from .models import SpecialPage, ContentLog, Announcement
from .forms import FirstRegisterForm

def index(request):
    announcements = Announcement.objects.order_by('-created_at')[:5]
    params = {
        'content_log': ContentLog(LIST_NUM=5),
        'announcements': announcements,
    }
    return render(request, 'home/index.html', params)

def login(request):
    params = {
    
    }
    if 'next' in request.GET:
        params['next'] = request.GET['next'] 
    return render(request, 'admin/login.html', params)

def logoutview(request):
    logout(request)
    return_to = urlencode({'returnTo': request.build_absolute_uri('/')})
    logout_url = 'https://%s/v2/logout?client_id=%s&%s' % \
                 (settings.SOCIAL_AUTH_AUTH0_DOMAIN, settings.SOCIAL_AUTH_AUTH0_KEY, return_to)
    return HttpResponseRedirect(logout_url)

def special(request, url):
    # keyは平文なので安全性は確保できないので注意
    # Google DriveとかでURLシェアするときと同等のセキュリティーだと考えたい。
    page = get_object_or_404(SpecialPage, url=url)    
    if 'k' in request.GET:
        k = request.GET['k']
        if k == page.key:
            return render(request, 'special/' + page.html_name)
    raise Http404

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