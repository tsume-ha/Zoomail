from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import logout
from django.contrib import messages
from django.shortcuts import redirect

def index(request):
    params = {
    
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