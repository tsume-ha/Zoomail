from django.shortcuts import render
from django.http import HttpResponse, Http404, FileResponse
from django.http.response import JsonResponse
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages as django_messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.utils.safestring import mark_safe
from django.utils.html import linebreaks, urlize

from django.conf import settings

from .models import Message, Bookmark, ToGroup
from .forms import MessageForm, AttachmentForm
from members.models import User

# html formatter
def target_blank(content):
    content = content.replace("<a ", '<a target="_blank" rel="nofollow ugc noopener" class="text-break" ')
    return mark_safe(content)


# 送信先グループ（全回・回生）の取得
def tos():
    return [(item.year, item.text()) for item in ToGroup.objects.filter(year=0)] + [
        (item.year, item.text()) for item in ToGroup.objects.filter(year__gt=0).order_by("year").reverse()
    ]


@login_required()
def get_messages_list(request):
    # import time
    # time.sleep(10)
    now_user = request.user

    if "page" in request.GET:
        try:
            page_num = int(request.GET["page"])
        except ValueError:
            page_num = 1
    else:
        page_num = 1

    query = Message.objects.filter(
        Q(years__year=now_user.year) | Q(years__year=0) | Q(sender=now_user) | Q(writer=now_user)
    ).order_by("updated_at")

    # 検索クエリ
    if "text" in request.GET:
        q = request.GET["text"]
        if q != "":
            query = query.filter(Q(content__contains=q) | Q(title__contains=q))
    if "is_kaisei" in request.GET:
        if request.GET["is_kaisei"] == "true":
            query = query.filter(years__year=now_user.year)
    if "is_zenkai" in request.GET:
        if request.GET["is_zenkai"] == "true":
            query = query.filter(years__year=0)
    if "is_bookmark" in request.GET:
        if request.GET["is_bookmark"] == "true":
            query = query.filter(bookmark_message__user=now_user)
    if "is_sender" in request.GET:
        if request.GET["is_sender"] == "true":
            query = query.filter(Q(sender=now_user) | Q(writer=now_user))

    query = query.reverse()

    page = Paginator(query, 30)

    return JsonResponse(
        {
            "messages": [
                {
                    "id": mes.id,
                    "title": mes.title,
                    "content": str(mes.content)[:100],
                    "html": target_blank(urlize(linebreaks(mes.content))),
                    "sender": mes.sender.get_short_name() if mes.sender else "削除されたユーザー",
                    "writer": mes.writer.get_short_name() if mes.writer else "削除されたユーザー",
                    "created_at": mes.created_at.strftime("%Y/%m/%d %H:%M"),
                    "updated_at": mes.updated_at.strftime("%Y/%m/%d %H:%M"),
                    "is_bookmarked": mes.bookmark_message.filter(user=now_user).exists(),
                    "attachments": [
                        {
                            "id": attachment.id,
                            "path": attachment.attachment_file.url,
                            "is_image": attachment.isImage(),
                            "filename": attachment.fileName(),
                            "fileext": attachment.extension(),
                        }
                        for attachment in mes.attachments.all()
                    ],
                }
                for mes in page.get_page(page_num)
            ],
            "paginator": {"now": page_num, "total": page.num_pages},
        }
    )


@login_required()
def get_one_message(request, id):
    # attachment, permissionなどのデータ
    message = get_object_or_404(Message, id=id)
    now_user = request.user

    # 閲覧できないならば/read にリダイレクトする
    if not message.years.filter(Q(year=now_user.year) | Q(year=0)).exists():
        if message.sender != now_user:
            if message.writer != now_user:
                raise PermissionDenied

    return JsonResponse(
        {
            "id": message.id,
            "title": message.title,
            "content": str(message.content)[:100],
            "html": target_blank(urlize(linebreaks(message.content))),
            "sender": message.sender.get_short_name() if message.sender else "削除されたユーザー",
            "writer": message.writer.get_short_name() if message.writer else "削除されたユーザー",
            "created_at": message.created_at.strftime("%Y/%m/%d %H:%M"),
            "updated_at": message.updated_at.strftime("%Y/%m/%d %H:%M"),
            "is_bookmarked": message.bookmark_message.filter(user=now_user).exists(),
            "attachments": [
                {
                    "id": attachment.id,
                    "path": attachment.attachment_file.url,
                    "is_image": attachment.isImage(),
                    "filename": attachment.fileName(),
                    "fileext": attachment.extension(),
                }
                for attachment in message.attachments.all()
            ],
        }
    )


@login_required()
def get_message_attachments(request, id):
    # attachment, permissionなどのデータ
    message = get_object_or_404(Message, id=id)
    now_user = request.user

    # 閲覧できないならば/read にリダイレクトする
    if not message.years.filter(Q(year=now_user.year) | Q(year=0)).exists():
        if message.sender != now_user:
            if message.writer != now_user:
                raise PermissionDenied

    return JsonResponse(
        {
            "attachments": [
                {
                    "path": file.attachment_file.url,
                    "is_image": file.isImage(),
                    "filename": file.fileName(),
                    "pk": file.pk,
                    "fileext": file.extension(),
                }
                for file in message.attachments.all()
            ]
        }
    )


# send from, to 選択肢
@login_required()
def to_groups_data(request):
    return JsonResponse({"togropus": [{"year": year, "label": text} for year, text in tos()]})


@login_required()
def froms_data(request):
    years = [y["year"] for y in User.objects.order_by("year").values("year").distinct()]
    return JsonResponse(
        {
            "years": years,
            "members": [
                {
                    "year": year,
                    "list": [
                        {"id": user.id, "name": user.get_short_name(), "year": user.year}
                        for user in User.objects.filter(year=year).order_by("furigana")
                    ],
                }
                for year in years
            ],
        }
    )


@login_required()
def bookmarkAPI(request, pk):
    now_user = request.user
    if request.method == "POST":
        if Bookmark.objects.filter(message_id__pk=pk).filter(user=now_user).exists():
            content = Bookmark.objects.filter(message_id__pk=pk).filter(user=now_user)
            content.delete()
            bookmark = "false"
        else:
            message = get_object_or_404(Message, pk=pk)
            content = Bookmark(message=message, user=now_user)
            content.save()
            bookmark = "true"
        return JsonResponse({"updated-to": bookmark})


@login_required()
def sendAPI(request):
    if request.method != "POST":
        return HttpResponse("Bad request", status=400)
    message_form = MessageForm(request.POST)
    message_form.fields["to"].choices = tos()
    if not message_form.is_valid():
        django_messages.error(request, "メーリスを送信できませんでした。")
        django_messages.error(request, message_form.errors.as_text())
        return HttpResponse("Bad request", status=400)
    else:
        message = message_form.save(commit=False)
        message.sender = request.user
        message.save()

        attachment_form = AttachmentForm(request.POST, request.FILES)
        if not attachment_form.is_valid():
            message.delete()
            django_messages.error(request, "添付ファイルにエラーがあり、メーリスを送信できませんでした。")
            django_messages.error(request, attachment_form.errors.as_text())
            return HttpResponse("400", status=400)
        else:
            attachment_form.save(message=message)
            # 独自実装: save()

        for to in message_form.cleaned_data["to"]:
            message.years.create(year=to)

        # sendgrid mail
        if settings.SEND_MAIL is not True:
            django_messages.info(request, "メール送信のsettingがFalseなので、メールは送信されませんでした。")
            return JsonResponse({"total_send_num": 0, "response": "SEND_MAIL was False."})

        from utils.mail import MailingList

        client = MailingList()
        total_send_num = client.send(message)
        django_messages.success(request, "メーリスを送信しました。")
        return JsonResponse({"total_send_num": total_send_num, "response": "done"})


@login_required()
def AttachmentDownloadView(request, message_id, attachment_id):
    message = get_object_or_404(Message, id=message_id)
    user = request.user

    # 閲覧できるか判定
    if not message.years.filter(Q(year=user.year) | Q(year=0)).exists():
        if message.sender != user:
            if message.writer != user:
                raise PermissionDenied
    # 添付ファイルを取得
    try:
        attachment = message.attachments.get(id=attachment_id)
    except ObjectDoesNotExist:
        raise Http404("Required attachment file does not exist")

    return FileResponse(
        open(attachment.attachment_file.path, "rb"),
        as_attachment=False,
        filename=message.title + "_添付" + attachment.extension()
        # TO DO ファイル名をデータベースに保存しておく
    )
