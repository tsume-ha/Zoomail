from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.datastructures import MultiValueDictKeyError
from django.db.models import Q
from .models import Message, MessageYear
from .forms import SendMessage, Search, DivErrorList
import datetime

@login_required(login_url='/admin/login/')
def index(request):
    # ログインしているユーザーの年度だけ含める
    query = Message.objects.filter(
        Q(years__year=request.user.year) | Q(years__year=0))

    if (request.method == 'POST'):
        str = request.POST['text']
        query = query.filter(Q(years__year=request.user.year) | Q(
            years__year=0)).filter(Q(content__contains=str) | Q(title__contains=str))

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

@login_required(login_url='/admin/login/')
def content(request, id):
    message = get_object_or_404(Message, id=id)

    # 閲覧できないならば/read にリダイレクトする
    if not message.years.all().filter(Q(year=request.user.year)|Q(year=0)).exists():
        return redirect('/read')

    attachments = map(
        lambda file: {"path": file.attachment_file, "isImage": file.isImage(), "fileName": file.fileName()},
        message.attachments.all()
    )
    params = {
        'message': message,
        'attachments': attachments
    }
    return render(request, 'board/content.html', params)

@login_required(login_url='/admin/login/')
def send(request):
    messageForm = SendMessage(request.POST or None, request.FILES or None, error_class=DivErrorList)
    params = {
        'message_form': messageForm,
    }
    if (request.method == 'POST'):
        if not messageForm.is_valid():
            # validation error 宛先未選択　ファイルサイズオーバー
            params['JSstop'] = True
            return render(request, 'board/send.html', params)
        else:
            to = request.POST["to"]
            title = request.POST["title"]
            content = request.POST["content"]
            nowtime = datetime.datetime.now()
            now_user = request.user
            try:
                file = request.FILES["attachmentfile"]
                is_attachment = True
            except MultiValueDictKeyError:
                is_attachment = False

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
            if is_attachment == True:
                content_data.attachments.create(attachment_file=file)
            return redirect(to='../read/')

    return render(request, 'board/send.html', params)
