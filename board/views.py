from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.db.models import Q
from .models import Message, MessageYear
from .forms import SendMessage, Search, Attachment

import datetime

def index(request):
    if (request.method == 'POST'):
        str = request.POST['text']
        data = Message.objects.filter(Q(content__contains=str) | Q(
            title__contains=str)).order_by('updated_at').reverse()
    else:
        data = Message.objects.all().order_by('updated_at').reverse()  # 逆順で取得

    textmax = 80
    for record in data:
        textrange = len(record.content)
        count = record.content.find('\n')
        record.content = record.content[count:count+textmax].replace('\n', ' ')
        if textrange > textmax:
            record.content += ' ...'
    params = {
        'search': Search(),
        'data': data,

    }
    return render(request, 'board/index.html', params)


def content(request, cont_num):
    data = Message.objects.get(id=cont_num)
    params = {
        'data': data,
    }
    return render(request, 'board/content.html', params)


def send(request):
    params = {
        'message_form': SendMessage(),
        'message_attachment': Attachment(),
    }
    if (request.method == 'POST'):
        title = request.POST["title"]
        to = request.POST["to"]
        content = request.POST["content"]
        nowtime = datetime.datetime.now()
        now_user = request.user

        if request.POST["attachment"] == "on":
            attachment = True
            file = request.FILES["select_file"]
            content_data = Message(
                title=title,
                content=content,
                attachment=attachment,
                sender_id=now_user,
                writer_id=now_user,
                created_at=nowtime,
                updated_at=nowtime
            )
            content_data.save()
            content_data.years.create(year=to)
            content_data.attachments.create(attachment_file=file)
        else:
            attachment = False
            content_data = Message(
                title=title,
                content=content,
                attachment=attachment,
                sender_id=now_user,
                writer_id=now_user,
                created_at=nowtime,
                updated_at=nowtime
            )
            content_data.save()
            content_data.years.create(year=to)
        content_data.save()

        return redirect(to='../read/')
    return render(request, 'board/send.html', params)
