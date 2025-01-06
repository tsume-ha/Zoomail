from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.views.decorators.http import require_http_methods

from ..models import Message


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
def detail(request, id):
    message = get_object_or_404(Message, id=id)
    context = {"message": message}
    return render(request, "mail/detail.html", context)
