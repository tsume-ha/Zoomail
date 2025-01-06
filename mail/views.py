from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.views.decorators.http import require_http_methods

from .models import Message
from .forms import MessageForm, AttachmentFormset


@require_http_methods(["GET"])
@login_required
def inbox(request):
    messages = (
        Message.objects.filter(
            Q(to_groups__year=0)
            | Q(to_groups__year=request.user.year)
            | Q(sender=request.user)
            | Q(writer=request.user)
        )
        .distinct()
        .order_by("-created_at")
    )

    # ページネーションの設定 (1ページに10件表示)
    paginator = Paginator(messages, 10)
    page_number = request.GET.get("page")  # URLの?page=からページ番号を取得
    page_obj = paginator.get_page(page_number)  # ページオブジェクトを取得

    # ページが複数ある場合はis_paginatedをTrueに設定
    is_paginated = page_obj.has_other_pages()

    context = {
        "messages": page_obj,  # ページネートされたメッセージ
        "page_obj": page_obj,  # ページネーション情報
        "is_paginated": is_paginated,  # ページが複数あるかどうか
    }
    return render(request, "mail/inbox.html", context)


@require_http_methods(["GET"])
@login_required
def mail_detail(request, message_id):
    message = Message.objects.get(id=message_id)
    context = {"message": message}
    return render(request, "mail/mail_detail.html", context)


@require_http_methods(["GET", "POST"])
@login_required
def send(request):
    if request.method == "GET":
        message_form = MessageForm()
        attachment_form = AttachmentFormset()
        context = {
            "message_form": message_form,
            "attachment_form": attachment_form,
        }
        return render(request, "mail/send.html", context)

    if request.method == "POST":
        message_form = MessageForm(request.POST)
        attachment_form = AttachmentFormset(request.POST, request.FILES)

        if message_form.is_valid() and attachment_form.is_valid():
            message = message_form.save(commit=False)
            message.sender = request.user
            message.save()
            attachments = attachment_form.save(commit=False)
            for attachment in attachments:
                attachment.message = message
                attachment.org_filename = attachment.file.name
                attachment.save()

            messages.success(request, "メッセージが正常に作成されました。")
            return redirect("mail:inbox")
        else:
            messages.error(request, "入力にエラーがあります。")
            context = {
                "message_form": message_form,
                "attachment_form": attachment_form,
            }
            return render(request, "mail/send.html", context)
