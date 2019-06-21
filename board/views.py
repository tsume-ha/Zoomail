from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from .models import Messages
from .forms import SendMessage

import datetime

def index(request):
	data = Messages.objects.all().order_by('id').reverse() #逆順で取得
	params = {
		'search':'検索とかそういうの - 開発中',
		'data':data,
	}
	return render(request, 'board/index.html', params)

def content(request, cont_num):
	data = Messages.objects.get(id=cont_num)
	params = {
		'data':data,
	}
	return render(request, 'board/content.html', params)

def send(request):
	params = {
		'form':SendMessage(),
	}
	if (request.method == 'POST'):
		title = request.POST["title"]
		to = request.POST["to"]
		content = request.POST["content"]
		nowtime = datetime.datetime.now()
		data = Messages(title=title, content=content, attaciment=False, sender_id=1, writer_id=1, created_at=nowtime, updated_at=nowtime)
		data.save()
		return redirect(to='../read/')
	return render(request, 'board/send.html', params)