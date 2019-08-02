from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.db.models import Q
from .models import Message, MessageYear
from .forms import SendMessage, Search, Attachment

import datetime

def index(request):
    # ログインしているユーザーの年度だけ含める
    query = Message.objects.filter(Q(years__year = request.user.year) | Q(years__year = -1))

    if (request.method == 'POST'):
        str = request.POST['text']
        query = query.filter(Q(years__year = request.user.year) | Q(years__year = -1)).filter(Q(content__contains=str) | Q(title__contains=str))

    messages = query.order_by('updated_at').reverse()  # 逆順で取得

    textmax = 80
    for message in messages:
        textrange = len(message.content)
        count = message.content.find('\n')
        message.content = message.content[count:count+textmax].replace('\n', ' ')
        if textrange > textmax:
            message.content += ' ...'
    params = {
        'search': Search(),
        'messages': messages,
    }
    return render(request, 'board/index.html', params)


def content(request, id):
    message = Message.objects.get(id=id)

    # 閲覧できないならば/read にリダイレクトする
    if not message.years.all().filter(Q(year=request.user.year)|Q(year=-1)).exists():
        return redirect('/read')

    params = {
        'message': message,
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
        is_attachment = request.POST.get('attachment', '') == 'on'
        content_data = Message(
            title=title,
            content=content,
            attachment=is_attachment,
            sender_id=now_user,
            writer_id=now_user,
            created_at=nowtime,
            updated_at=nowtime
        )
        content_data.save()
        content_data.years.create(year=to)
        if is_attachment:
            file = request.FILES["select_file"]
            content_data.attachments.create(attachment_file=file)
        content_data.save()

        return redirect(to='../read/')
    return render(request, 'board/send.html', params)
