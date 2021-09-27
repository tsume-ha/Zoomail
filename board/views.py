import logging
import base64

from django.shortcuts import render
from django.http import HttpResponse
from django.http.response import JsonResponse
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, To, PlainTextContent, FileContent, FileName, FileType, Disposition
from sendgrid.helpers.mail import Attachment as helper_Attachment

from django.conf import settings

from .models import Message, MessageYear, Attachment, Bookmark, ToGroup
from .forms import MessageForm
from members.models import User
from mail.models import SendMailAddress, MessageProcess

# 送信先グループ（全回・回生）の取得
def tos():
    return[
        (item.year, item.text()) for item in ToGroup.objects.filter(year=0)
    ] + [
        (item.year, item.text()) for item in ToGroup.objects.filter(year__gt=0).order_by("year").reverse()
    ]

@login_required()
def get_messages_list(request):
    now_user = request.user

    if 'page' in request.GET:
        try:
            page_num = int(request.GET['page'])
        except ValueError:
            page_num = 1
    else:
        page_num = 1

    query = Message.objects.filter(
        Q(years__year=now_user.year) | Q(years__year=0) | Q(sender=now_user) | Q(writer=now_user)
        ).order_by('updated_at')

    # 検索クエリ
    if 'text' in request.GET:
        q = request.GET['text']
        if q != '':
            query = query.filter(Q(content__contains=q) | Q(title__contains=q))
    if 'is_kaisei' in request.GET:
        if request.GET['is_kaisei'] == 'true':
            query = query.filter(years__year=now_user.year)
    if 'is_zenkai' in request.GET:
        if request.GET['is_zenkai'] == 'true':
            query = query.filter(years__year=0)
    if 'is_bookmark' in request.GET:
        if request.GET['is_bookmark'] == 'true':
            query = query.filter(bookmark_message__user=now_user)
    if 'is_sender' in request.GET:
        if request.GET['is_sender'] == 'true':
            query = query.filter(
                Q(sender=now_user) | Q(writer=now_user)
            )

    query = query.reverse()

    page = Paginator(query, 10)

    params = {
        'page': page.get_page(page_num),
    }
    return render(request, 'board/messages.json', params, content_type='application/json')


@login_required()
def get_one_message(request, id):
    # attachment, permissionなどのデータ
    message = get_object_or_404(Message, id=id)
    now_user = request.user

    # 閲覧できないならば/read にリダイレクトする
    if not message.years.filter(Q(year=now_user.year)|Q(year=0)).exists():
        if message.sender != now_user:
            if message.writer != now_user:
                raise PermissionDenied

    params = {
        'message': message,
    }
    return render(request, 'board/message.json', params, content_type='application/json')


@login_required()
def get_message_attachments(request, id):
    # attachment, permissionなどのデータ
    message = get_object_or_404(Message, id=id)
    now_user = request.user

    # 閲覧できないならば/read にリダイレクトする
    if not message.years.filter(Q(year=now_user.year)|Q(year=0)).exists():
        if message.sender != now_user:
            if message.writer != now_user:
                raise PermissionDenied

    return JsonResponse({
        "attachments": [{
            "path": file.attachment_file.url,
            "is_image": file.isImage(),
            "filename": file.fileName(),
            "pk": file.pk,
            "fileext": file.extension()
        } for file in message.attachments.all()]
    })


# send from, to 選択肢
@login_required()
def to_groups_data(request):
    return JsonResponse({
        "togropus": [{"year": year, "label": text} for year, text in tos()]
    })


@login_required()
def froms_data(request):
    years = [y['year'] for y in User.objects.order_by('year').values('year').distinct()]
    return JsonResponse({
        "years": years,
        "members": [{
        "year": year,
        "list": [{
            "id": user.id,
            "name": user.nickname if user.nickname else user.last_name + user.first_name# get_short_nameは使えない
            } for user in User.objects.filter(year=year).order_by('furigana')]
        } for year in years],
        "user": {
            "year": request.user.year,
            "id": request.user.id
        }
    }, safe=False)


@login_required()
def bookmarkAPI(request, pk):
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
        return JsonResponse({
            'updated-to': bookmark
        })


@login_required()
def sendAPI(request):
    logger = logging.getLogger(__name__)
    logger.info('Send API called')
    message_form = MessageForm(request.POST)
    message_form.fields["to"].choices = tos()
    if request.method == 'POST' and message_form.is_valid():
        message = message_form.save(commit=False)
        message.sender = request.user
        message.save()
        logger.info(message.title)

        filelist = request.FILES.getlist('attachments')
        if filelist:
            for file in filelist:
                if file.size > 10*1024*1024:
                    message.delete()
                    return HttpResponse('400', status=400)
                attachment = Attachment(attachment_file=file, message=message)
                attachment.save()

        for to in message_form.cleaned_data["to"]:
            message.years.create(year=to)

        # sendgrid mail
        if settings.SEND_MAIL is not True:
            return JsonResponse({
                "total_send_num": 0,
                "response": "SEND_MAIL was False."
            })
        year_query = MessageYear.objects.filter(message=message).values('year')

        if year_query.filter(year=0).exists():
            from_email_adress = 'zenkai@message.ku-unplugged.net'
            to_list = SendMailAddress.objects.all().values_list('email', flat=True)
            mail_compose(from_email_adress, to_list, message)

        else:
            ordinal = lambda n: "%d%s" % (n,"tsnrhtdd"[(n/10%10!=1)*(n%10<4)*n%10::4])
            for year in year_query:
                from_email_adress = ordinal(int(year['year']) - 1994) + '_kaisei@message.ku-unplugged.net'
                to_list = SendMailAddress.objects.filter(year=year['year']).values_list('email', flat=True)
                mail_compose(from_email_adress, to_list, message)

        total_send_num = MessageProcess.objects.filter(message=message, Requested=True, Error_occurd=False).count()
        return JsonResponse({
            "total_send_num": total_send_num,
            "response": ""
        })


    return HttpResponse('Bad request', status=400)



def mail_compose(from_email_adress, to_list, message_data):
    '''
    宛先リストとメッセージコンテントからメールを構成、送信するところまで行う。

    Parameters
    ----------
    from_email_adress: str
        送信元のメールアドレス
        全回なら'zenkai@message.ku-unplugged.net'
    to_list: list
        emailアドレスのリスト
    message_data: Query Object
        board.models.Message のオブジェクト
    '''

    logger = logging.getLogger(__name__)
    logger.info('mail_compose called')
    subject = message_data.title
    text_content = message_data.content

    added_text = '\n\n--------------------------------\nこのメッセージのURLはこちら\nhttps://message.ku-unplugged.net/read/content/' + str(message_data.pk)

    from_email_name = message_data.writer.get_short_name()
    to_emails = [To(email=eml) for eml in to_list]
    message = Mail(
        from_email=(from_email_adress, from_email_name),
        to_emails=to_emails,
        subject=subject,
        plain_text_content=PlainTextContent(text_content + added_text),
        is_multiple=True
        )
    
    is_attachment = Attachment.objects.filter(message=message_data).exists()
    if is_attachment:
        file_list = Attachment.objects.filter(message=message_data).order_by('id').reverse()
        attachment_list = []
        for file in file_list:
            file_path = file.attachment_file.path
            with open(file_path, 'rb') as f:
                a_data = f.read()
                f.close()
            encoded = base64.b64encode(a_data).decode()
            attachment = helper_Attachment(
                file_content = FileContent(encoded),
                file_type = FileType('application/octet-stream'),
                file_name = FileName(file.fileName()),
                disposition = Disposition('attachment'),
                )
            attachment_list.append(attachment)

        message.attachment = attachment_list

    # message.send_at = int(datetime.datetime.now().timestamp() + 100)

    try:
        logger.info('try sending begin')
        sendgrid_client = SendGridAPIClient(settings.SENDGRID_API_KEY)
        response = sendgrid_client.send(message)
        x_message_id = response.headers['X-Message-Id']

        requested = True
        error_occurd = False
        error_detail = ''

    except Exception as e:
        logger.info('try sending error')
        x_message_id = ''
        requested = False
        error_occurd = True
        error_detail = e

    finally:
        logger.info('before bulk create')
        process_list = []
        for email in to_list:
            obj = MessageProcess(
                message=message_data,
                x_message_id=x_message_id,
                email=email,
                Requested=requested,
                Error_occurd=error_occurd,
                Error_detail=error_detail,
                )
            process_list.append(obj)
        MessageProcess.objects.bulk_create(process_list)
    print(response)
    logger.info('after bulk create')
    return response



from utils.commom import download
@login_required()
def FileDownloadView(request, message_pk, file_pk):
    try:
        message = Message.objects.get(pk=message_pk)
        file = Attachment.objects.get(pk=file_pk)
        year = MessageYear.objects.get(message=message).year
    except ObjectDoesNotExist:
        return redirect('/read/content/' + str(message_pk))

    can_read = (year == 0) or (year == request.user.year)\
               or (message.writer == request.user)\
               or (message.sender == request.user)
    if not can_read:
        return redirect('/read/content/' + str(message_pk))

    filename = message.title + '_添付' + file.extension()
    response = download(
        filepath = file.attachment_file.path,
        filename = filename,
        mimetype = 'application/octet-stream'
    )
    return response
