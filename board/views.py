from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages as django_messages
from django.utils.datastructures import MultiValueDictKeyError
from django.db.models import Q
from django.core.paginator import Paginator
from django.core.exceptions import PermissionDenied
from .models import Message, MessageYear, Attachment, Kidoku, Bookmark
from .forms import SendMessage, SearchAdvanced, Edit, AttachmentFileFormset
from members.models import User
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, To, PlainTextContent
from config.settings_local import SENDGRID_API_KEY
from django.conf import settings
import datetime

def EditPermisson(user, content_id):
    return user.is_superuser or\
           Message.objects.get(id=content_id).sender == user or\
           Message.objects.get(id=content_id).writer == user

def is_updated(created_at, updated_at):
    return created_at + datetime.timedelta(seconds=5) < updated_at

@login_required()
def index(request, page_num=1):
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

    querydict = dict(request.GET)
    getquery = ''
    for key, value in querydict.items():
        if value[0] == "":
            continue
        tmp = key + '=' + value[0]
        getquery += '&' + tmp
    params = {
        'search_advanced': SearchAdvanced(request.GET),
        'message_letters': page.get_page(page_num),
        'is_seached': searched,
        'getquery': getquery,
    }
    return render(request, 'board/index.html', params)

@login_required()
def content(request, id):
    message = get_object_or_404(Message, id=id)
    now_user = request.user

    # 閲覧できないならば/read にリダイレクトする
    if not message.years.all().filter(Q(year=now_user.year)|Q(year=0)).exists():
        if not EditPermisson(now_user, id):
            raise PermissionDenied


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
        kidoku_content = Kidoku(message=message, user=now_user)
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
        'attachment_form': AttachmentFileFormset(),
    }
    if (request.method == 'POST'):
        if messageForm.is_valid():
            to_list = request.POST.getlist("to")
            writer_pk = request.POST["written_by"]
            title = request.POST["title"]
            content = request.POST["content"]
            nowtime = datetime.datetime.now()
            now_user = request.user
            content_data = Message(
                title=title,
                content=content,
                sender=now_user,
                writer=User.objects.get(pk=int(writer_pk[5:])),
                updated_at=nowtime,
                created_at=nowtime,
            )
            formset = AttachmentFileFormset(request.POST, files=request.FILES, instance=content_data)
            if formset.is_valid():
                content_data.save()
                formset.save()
                for to in to_list:
                    content_data.years.create(year=to)

                # sendgrid mail
                subject = content_data.title
                text_content = content_data.content
                is_attachment = Attachment.objects.filter(message=content_data).exists()
                if is_attachment:
                    text_content += '\n\n--------------------------------\n※このメッセージには添付ファイルがあります。\n※添付ファイルはメーリスHPにアクセスして見てください。\n\nこのメッセージのURLはこちら\nhttps://message.ku-unplugged.net/read/content/' + str(content_data.pk)
                else:
                    text_content += '\n\n--------------------------------\nこのメッセージのURLはこちら\nhttps://message.ku-unplugged.net/read/content/' + str(content_data.pk)
                year_query = MessageYear.objects.filter(message=content_data).values('year')

                if year_query.filter(year=0).exists():
                    from_email_adress = 'zenkai@message.ku-unplugged.net'
                    from_email_name = content_data.writer.get_short_name()
                    to_list = User.objects.all().values_list('receive_email', flat=True)
                    to_emails = [To(email=eml) for eml in to_list]
                    send_massage_data = Mail(
                        from_email=(from_email_adress, from_email_name),
                        to_emails=to_emails,
                        subject=subject,
                        plain_text_content=PlainTextContent(text_content),
                        is_multiple=True
                        )
                    if settings.SEND_MAIL == True:
                        try:
                            sendgrid_client = SendGridAPIClient(SENDGRID_API_KEY)
                            response = sendgrid_client.send(send_massage_data)
                        except Exception as e:
                            print(e.message)

                else:
                    ordinal = lambda n: "%d%s" % (n,"tsnrhtdd"[(n/10%10!=1)*(n%10<4)*n%10::4])
                    for year in year_query:
                        from_email_adress = ordinal(int(year['year']) - 1994) + '_kaisei@message.ku-unplugged.net'
                        from_email_name = content_data.writer.get_short_name()
                        if not User.objects.filter(year=year['year']).exists():
                            continue
                        to_list = User.objects.filter(year=year['year']).values_list('receive_email', flat=True)
                        to_emails = [To(email=eml) for eml in to_list]
                        send_massage_data = Mail(
                            from_email=(from_email_adress, from_email_name),
                            to_emails=to_emails,
                            subject=subject,
                            plain_text_content=PlainTextContent(text_content),
                            is_multiple=True
                            )
                        if settings.SEND_MAIL == True:
                            try:
                                sendgrid_client = SendGridAPIClient(SENDGRID_API_KEY)
                                response = sendgrid_client.send(send_massage_data)
                            except Exception as e:
                                print(e.message)

                django_messages.success(request, 'メッセージを送信しました。 件名 : '+title)

                return redirect(to='../read/')
            else:
                django_messages.error(request, 'どの添付ファイルのサイズも30MB未満にしてください')
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
                    content = editForm.save(commit=False)
                    content.updated_at = datetime.datetime.now()
                    content.save()
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