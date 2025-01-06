from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.views.decorators.http import require_http_methods

from ..models import Message
from ..forms import MessageForm, AttachmentFormset


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
