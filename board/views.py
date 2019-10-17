from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages as django_messages
from django.utils.datastructures import MultiValueDictKeyError
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Message, MessageYear, Attachment, Kidoku, Bookmark
from .forms import SendMessage, SearchAdvanced, Edit
from members.models import User
import datetime
import urllib.parse

def EditPermisson(user, content_id):
    return user.is_superuser or\
           Message.objects.get(id=content_id).sender == user or\
           Message.objects.get(id=content_id).writer == user

def is_updated(created_at, updated_at):
    return created_at + datetime.timedelta(seconds=5) < updated_at

@login_required()
def index(request):
    now_user = request.user
    # ログインしているユーザーの年度だけ含める
    query = Message.objects.filter(Q(years__year=now_user.year) | Q(years__year=0))

    searched = False
    if 'text' in request.GET:
        q = request.GET['text']
        if q != '':
            query = query.filter(Q(content__contains=q) | Q(title__contains=q))
            searched = True
    if 'is_kaisei' in request.GET:
        if request.GET['is_kaisei'] == 'on':
            query = query.filter(years__year=now_user.year)
            searched = True
    if 'is_zenkai' in request.GET:
        if request.GET['is_zenkai'] == 'on':
            query = query.filter(years__year=0)
            searched = True
    if 'is_midoku' in request.GET:
        if request.GET['is_midoku'] == 'on':
            query = query.exclude(kidoku_message__user=now_user)
            searched = True
    if 'is_marked' in request.GET:
        if request.GET['is_marked'] == 'on':
            query = query.filter(bookmark_message__user=now_user)
            searched = True

    message_letters = query.order_by('updated_at').reverse()  # 逆順で取得
    page = Paginator(message_letters, 10)


    if 'page' in request.GET:
        num = request.GET['page']
    else:
        num = 1
    
    params = {
        'search_advanced': SearchAdvanced(request.GET),
        'message_letters': page.get_page(num),
        'is_seached': searched,
    }
    return render(request, 'board/index.html', params)

@login_required()
def content(request, id):
    message = get_object_or_404(Message, id=id)
    now_user = request.user

    # 閲覧できないならば/read にリダイレクトする
    if not message.years.all().filter(Q(year=now_user.year)|Q(year=0)).exists():
        return redirect('/read')

    attachments = map(
        lambda file: {"path": file.attachment_file, "isImage": file.isImage(), "fileName": file.fileName(), "pk": file.pk, "fileext": file.extension()},
        message.attachments.all()
    )
    params = {
        'message': message,
        'attachments': attachments,
        'edit_allowed': EditPermisson(user=now_user, content_id=id),
        'is_updated': is_updated(message.created_at, message.updated_at),
    }

    if not Kidoku.objects.filter(message=message).filter(user=now_user).exists():
        kidoku_content = Kidoku(message=message, user=now_user, have_read=True)
        kidoku_content.save()

    return render(request, 'board/content.html', params)

@login_required()
def ajax_bookmark(request, pk):
    now_user = request.user
    if (request.method == 'POST'):
        if Bookmark.objects.filter(message_id__pk=pk).filter(user=now_user).exists():
            content = Bookmark.objects.filter(message_id__pk=pk).filter(user=now_user)
            content.delete()
            bookmark = 'false'
        else:
            message = get_object_or_404(Message, pk=pk)
            content = Bookmark(message=message, user=now_user)
            content.save()
            bookmark = 'true'
        return HttpResponse('bookmark='+bookmark)

@login_required()
def send(request):
    messageForm = SendMessage(
        request.POST or None,
        request.FILES or None,
        initial={'written_by': str(request.user.year)+'-'+str(request.user.pk),
                 'year_choice': request.user.year}
    )
    years = User.objects.order_by().values('year').distinct()
    messageForm.fields['year_choice'].choices = [(q['year'],q['year']) for q in years]
    messageForm.fields['written_by'].choices = [(str(user.year).zfill(4)+'-'+str(user.pk), user.get_full_name) for user in User.objects.all().order_by('year').order_by('furigana')]
    params = {
        'message_form': messageForm,
    }
    if (request.method == 'POST'):
        if messageForm.is_valid():
            to_list = request.POST.getlist("to")
            writer_pk = request.POST["written_by"]
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
                writer=User.objects.get(pk=int(writer_pk[5:])),
                updated_at=nowtime,
                created_at=nowtime,
            )
            content_data.save()
            for to in to_list:
                content_data.years.create(year=to)            
            if is_attachment == True:
                content_data.attachments.create(attachment_file=file)
            django_messages.success(request, 'メッセージを送信しました。 件名 : '+title)
            return redirect(to='../read/')

        else:
            # print('validation error')
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



from utils.commom import download
@login_required()
def FileDownloadView(request, message_pk, file_pk):
    try:
        message = Message.objects.get(pk=message_pk)
        file = Attachment.objects.get(pk=file_pk)
        year = MessageYear.objects.get(message=message).year
    except ObjectDoesNotExist:
        return redirect('/read/content/' + str(message_pk))

    can_read = year == 0 or year == request.user.year
    if not can_read:
        return redirect('/read/content/' + str(message_pk))

    filename = message.title + '_添付' + file.extension()
    response = download(
        filepath = file.attachment_file.path,
        filename = filename,
        mimetype = 'application/octet-stream'
    )
    return response