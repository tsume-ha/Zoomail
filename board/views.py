from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages as django_messages
from django.utils.datastructures import MultiValueDictKeyError
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Message, MessageYear, Attachment
from .forms import SendMessage, Search, Edit, DivErrorList
from members.models import User
from django.core.mail import send_mass_mail
import datetime

def EditPermisson(user, content_id):
    return user.is_superuser or\
           Message.objects.get(id=content_id).sender == user or\
           Message.objects.get(id=content_id).writer == user

def is_updated(created_at, updated_at):
    return created_at + datetime.timedelta(seconds=5) < updated_at

@login_required()
def index(request):

    # ログインしているユーザーの年度だけ含める
    query = Message.objects.filter(
        Q(years__year=request.user.year) | Q(years__year=0))

    searched = False
    if (request.method == 'POST'):
        str = request.POST['text']
        if (str != ''):            
            query = query.filter(Q(years__year=request.user.year) | Q(
                years__year=0)).filter(Q(content__contains=str) | Q(title__contains=str))
            searched = True

    message_letters = query.order_by('updated_at').reverse()  # 逆順で取得
    page = Paginator(message_letters, 10)


    if 'page' in request.GET:
        num = request.GET['page']
    else:
        num = 1
    
    params = {
        'search': Search(),
        'message_letters': page.get_page(num),
        'is_seached': searched,
    }
    return render(request, 'board/index.html', params)

@login_required()
def content(request, id):
    message = get_object_or_404(Message, id=id)

    # 閲覧できないならば/read にリダイレクトする
    if not message.years.all().filter(Q(year=request.user.year)|Q(year=0)).exists():
        return redirect('/read')

    attachments = map(
        lambda file: {"path": file.attachment_file, "isImage": file.isImage(), "fileName": file.fileName(), "pk": file.pk, "fileext": file.extension()},
        message.attachments.all()
    )
    params = {
        'message': message,
        'attachments': attachments,
        'edit_allowed': EditPermisson(user=request.user, content_id=id),
        'is_updated': is_updated(message.created_at, message.updated_at),
    }
    return render(request, 'board/content.html', params)

@login_required()
def send(request):
    messageForm = SendMessage(
        request.POST or None,
        request.FILES or None,
        error_class = DivErrorList,
        initial={'written_by': str(request.user.year)+'-'+str(request.user.pk),
                 'year_choice': request.user.year}
    )
    params = {
        'message_form': messageForm,
    }
    if (request.method == 'POST'):
        if messageForm.is_valid():
            to = request.POST["to"]
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
            content_data.years.create(year=to)
            if is_attachment == True:
                content_data.attachments.create(attachment_file=file)


            year = MessageYear.objects.get(message=content_data).year
            if year == 0:
                mail_list = [user.email for user in User.objects.all()]
            else:
                mail_list = [user.email for user in User.objects.filter(year=year)]
            datatuple = ((content_data.title, content_data.content, 'message@ku-unplugged.net', [subject_to])\
                for subject_to in mail_list)
            success_num = send_mass_mail(datatuple)

            django_messages.success(request, 'メッセージを送信しました。 件名 : '+title)
            django_messages.success(request, 'メール送信件数 : '+str(success_num))



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