from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from .models import PostTest
from .forms import SendMessage

import datetime

def index(request):
	data = PostTest.objects.all().order_by('id').reverse() #逆順で取得
	params = {
		'search':'検索とかそういうの - 開発中',
		'data':data,
	}
	return render(request, 'read_index.html', params)

def content(request, cont_num):
	data = PostTest.objects.get(id=cont_num)
	params = {
		'data':data,
	}
	return render(request, 'read_content.html', params)

def send(request):
	params = {
		'form':SendMessage(),
	}
	if (request.method == 'POST'):
		title = request.POST["title"]
		to = request.POST["to"]
		content = request.POST["content"]
		nowtime = datetime.datetime.now()
		data = PostTest(title = title, content = content, created_at = nowtime, whosend = 1, whopost = 1)
		data.save()
		return redirect(to='../read/')
	return render(request, 'send.html', params)