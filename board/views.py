from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.db.models import Q
from .models import Messages, Message_Year
from .forms import SendMessage, Search

import datetime

def index(request):
	if (request.method == 'POST'):
		str = request.POST['text']
		data = Messages.objects.filter(Q(content__contains=str)|Q(title__contains=str)).order_by('updated_at').reverse()
	else:
		data = Messages.objects.all().order_by('updated_at').reverse() #逆順で取得

	textmax = 80
	for record in data:
		textrange = len(record.content)
		count = record.content.find('\n')
		record.content = record.content[count:count+textmax].replace('\n', ' ')
		if textrange > textmax:
			record.content += ' ...'
	params = {
		'search':Search(),
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
		'message_form':SendMessage(),
	}
	if (request.method == 'POST'):
		title = request.POST["title"]
		to = request.POST["to"]
		content = request.POST["content"]
		nowtime = datetime.datetime.now()
		now_user = 1
		content_data = Messages(
			title=title,
			content=content,
			sender_id=now_user,
			writer_id=now_user,
			created_at=nowtime,
			updated_at=nowtime
		)
		content_data.save()
		tmp = Messages.objects.get(created_at=nowtime)
		year_data = Message_Year(mes_ID=tmp, year=to)
		year_data.save()

		return redirect(to='../read/')
	return render(request, 'board/send.html', params)