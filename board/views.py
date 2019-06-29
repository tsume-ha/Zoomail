from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.forms.models import inlineformset_factory
from .models import Messages, Message_Year
from .forms import SendMessage, SendTo

import datetime

def index(request):
	data = Messages.objects.all().order_by('id').reverse() #逆順で取得
	textlange = 120
	for record in data:
		count = record.content.find('\n')
		record.content = record.content[count:count+textlange].replace('\n', ' ')
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

# def send(request):
# 	params = {
# 		'form':SendMessage(),
# 	}
# 	if (request.method == 'POST'):
# 		title = request.POST["title"]
# 		to = request.POST["to"]
# 		content = request.POST["content"]
# 		nowtime = datetime.datetime.now()
# 		content_data = Messages(title=title, content=content, sender_id=1, writer_id=1, created_at=nowtime, updated_at=nowtime)
# 		content_data.save()

# 		return redirect(to='../read/')
# 	return render(request, 'board/send.html', params)


def send(request):
	SendInlineFormset = inlineformset_factory(
		parent_model = Messages,
		model = Message_Year,
		form = SendMessage,
		extra = 1
	)
	if request.method == 'POST':
		yearForm = SendTo(request.POST)

		if yearForm.is_valid():
			new_yearForm = yearForm.save(commit=False)
			sendInlineFormset = SendInlineFormset(request.POST, request.FILES, instance=new_yearForm)
			if sendInlineFormset.is_valid():
				sendInlineFormset.save()
				return redirect(to='../read/')
			else :
				classificationformset = ClassificationInlineFormSet(request.POST, request.FILES, instance=new_yearForm)
	else:
		sendInlineFormset = SendInlineFormset()
		yearForm = SendTo(request.POST)
	params = {
		'content_form': SendMessage(),
		'year_form': SendTo(),

	}
	return render(request, 'board/send.html', params)
				
				