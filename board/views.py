import logging

from django.shortcuts import render
from django.http import HttpResponse
from django.http.response import JsonResponse
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist

from django.conf import settings

from .models import Message, MessageYear, Attachment, Bookmark, ToGroup
from .forms import MessageForm
from members.models import User


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

        from utils.mail import MailingList
        client = MailingList()
        total_send_num = client.send(message)
        
        return JsonResponse({
            "total_send_num": total_send_num,
            "response": "done"
        })


    return HttpResponse('Bad request', status=400)



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
