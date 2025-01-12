from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.views.decorators.http import require_http_methods

from ..models import Message
from ..forms import InboxForm


@require_http_methods(["GET"])
@login_required
def inbox(request):
    messages = Message.objects.filter(
        Q(to_groups__year=0)
        | Q(to_groups__year=request.user.year)
        | Q(sender=request.user)
        | Q(writer=request.user)
    )

    form = InboxForm(request.GET or None, initial={"query": "all"})

    if form.is_valid():
        text: str | None = form.cleaned_data.get("text")
        query: str = form.cleaned_data.get("query", "all")  # queryが空ならallを渡す
        if query == "all":
            pass
        if query == "zenkai":
            messages = messages.filter(to_groups__year=0)
        if query == "kaisei":
            messages = messages.filter(to_groups__year=request.user.year)
        if query == "sender":
            messages = messages.filter(Q(sender=request.user) | Q(writer=request.user))

        if text:
            text = text.strip()
            text = text.replace("　", " ")
            text_list = text.split(" ")
            exclude_queries = Q()  # 除外条件用の Q オブジェクト
            include_queries = Q()  # 検索条件用の Q オブジェクト
            for t in text_list:
                if t.startswith("-"):  # 除外フィルタ
                    term = t[1:]  # 先頭の「-」を除去
                    exclude_queries |= Q(title__icontains=term) | Q(
                        content__icontains=term
                    )
                else:  # 通常検索フィルタ
                    include_queries |= Q(title__icontains=t) | Q(content__icontains=t)
            # フィルタを適用
            messages = messages.filter(include_queries).exclude(exclude_queries)

    messages = messages.distinct().order_by("-created_at")

    # ページネーションの設定 (1ページに10件表示)
    paginator = Paginator(messages, 10)
    page_number = request.GET.get("page")  # URLの?page=からページ番号を取得
    page_obj = paginator.get_page(page_number)  # ページオブジェクトを取得

    # ページが複数ある場合はis_paginatedをTrueに設定
    is_paginated = page_obj.has_other_pages()

    # print(form.query)
    context = {
        "mailis": page_obj,  # ページネートされたメッセージ
        # message framework と変数名が競合するため、ここではmailisとしている
        "page_obj": page_obj,  # ページネーション情報
        "is_paginated": is_paginated,  # ページが複数あるかどうか
        "form": form,
    }
    return render(request, "mail/inbox.html", context)


@require_http_methods(["GET"])
@login_required
def detail(request, id):
    message = get_object_or_404(Message, id=id)
    context = {"message": message}
    return render(request, "mail/detail.html", context)
