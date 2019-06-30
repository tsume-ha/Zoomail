from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.forms.models import inlineformset_factory
from .models import Messages, Message_Year
from .forms import SendMessage

import datetime

def index(request):
	data = Messages.objects.all().order_by('id').reverse() #逆順で取得
	textmax = 120
	for record in data:
		textrange = len(record.content)
		count = record.content.find('\n')
		record.content = record.content[count:count+textmax].replace('\n', ' ')
		if textrange > textmax:
			record.content += ' ...'
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