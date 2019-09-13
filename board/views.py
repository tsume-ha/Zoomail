from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages as django_messages
from django.utils.datastructures import MultiValueDictKeyError
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Message, MessageYear
from .forms import SendMessage, Search, Edit, DivErrorList
import datetime

def EditPermisson(user, content_id):
    return user.is_superuser or\
           Message.objects.get(id=content_id).sender == user or\
           Message.objects.get(id=content_id).writer == user


@login_required()
def index(request):
    # ログインしているユーザーの年度だけ含める
    query = Message.objects.filter(
        Q(years__year=request.user.year) | Q(years__year=0))

    if (request.method == 'POST'):
        str = request.POST['text']
        query = query.filter(Q(years__year=request.user.year) | Q(
            years__year=0)).filter(Q(content__contains=str) | Q(title__contains=str))

    message_letters = query.order_by('updated_at').reverse()  # 逆順で取得


    textmax = 80
    for message_letter in message_letters:
        if len(message_letter.content) < textmax:
            continue
        count = message_letter.content.find('\n')
        while message_letter.content[-2:-1] == '\n':
            message_letter.content = message_letter.content[:-3]
        message_letter.content = message_letter.content[count:].replace('\n', ' ')
        if len(message_letter.content) < textmax + 5:
            continue
        message_letter.content = message_letter.content[:textmax] + ' ...'

    page = Paginator(message_letters, 50)


    if 'page' in request.GET:
        num = request.GET['page']
    else:
        num = 1
    
    params = {
        'search': Search(),
        'message_letters': page.get_page(num),
    }
    return render(request, 'board/index.html', params)

@login_required()
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
        'attachments': attachments,
        'edit_allowed': EditPermisson(user=request.user, content_id=id)
    }
    return render(request, 'board/content.html', params)

@login_required()
def send(request):
    messageForm = SendMessage(request.POST or None, request.FILES or None, error_class=DivErrorList)
    params = {
        'message_form': messageForm,
    }
    if (request.method == 'POST'):
        if messageForm.is_valid():
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
                sender=now_user,
                writer=now_user,
                created_at=nowtime,
                updated_at=nowtime
            )
            content_data.save()
            content_data.years.create(year=to)
            if is_attachment == True:
                content_data.attachments.create(attachment_file=file)
            django_messages.success(request, 'メッセージを送信しました。 件名 : '+title)
            return redirect(to='../read/')

        else:
            # validation error
            params['JSstop'] = True

    return render(request, 'board/send.html', params)


@login_required()
def edit(request, id):
    before_edit = get_object_or_404(Message, id=id)
    if EditPermisson(user=request.user, content_id=id):
        editForm = Edit(request.POST or None, instance=before_edit)
        if (request.method == 'POST'):
            if editForm.is_valid:
                if request.POST['title'] != before_edit.title or request.POST['content'] != before_edit.content:
                    editForm.save()
                    django_messages.success(request, '更新しました')
                else:
                    django_messages.success(request, '変更はありませんでした')
                return redirect('/read/content/' + str(id))
            else:
                django_messages.error(request, '更新できませんでした')
        params = {
            'before_edit': before_edit,
            'EditForm': editForm,
        }
        return render(request, 'board/edit.html', params)
    else:
        return redirect('/read/content/' + str(id))

