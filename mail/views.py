from django.core.paginator import Paginator
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from .models import Message


@login_required
def inbox(request):
    messages = Message.objects.filter(
        Q(to_groups__year=0)
        | Q(to_groups__year=request.user.year)
        | Q(sender=request.user)
        | Q(writer=request.user)
    ).distinct()

    # ページネーションの設定 (1ページに10件表示)
    paginator = Paginator(messages, 10)
    page_number = request.GET.get("page")  # URLの?page=からページ番号を取得
    page_obj = paginator.get_page(page_number)  # ページオブジェクトを取得

    # ページが複数ある場合はis_paginatedをTrueに設定
    is_paginated = page_obj.has_other_pages()

    context = {
        "messages": page_obj,  # ページネートされたメッセージ
        "page_obj": page_obj,  # ページネーション情報
        "is_paginated": is_paginated or True,  # ページが複数あるかどうか
    }
    return render(request, "mail/inbox.html", context)


@login_required
def mail_detail(request, message_id):
    message = Message.objects.get(id=message_id)
    context = {"message": message}
    return render(request, "mail/mail_detail.html", context)
