from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.contrib.auth import logout
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from .models import SpecialPage, ContentLog
import os

def index(request):
    params = {
        'content_log': ContentLog(LIST_NUM=5),
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
    messages.success(request,"ログアウトしました。")
    return redirect(to='/')

def special(request, url):
    # keyは平文なので安全性は確保できないので注意
    # Google DriveとかでURLシェアするときと同等のセキュリティーだと考えたい。
    page = get_object_or_404(SpecialPage, url=url)    
    if 'k' in request.GET:
        k = request.GET['k']
        if k == page.key:
            return render(request, 'special/' + page.html_name)
    raise Http404
