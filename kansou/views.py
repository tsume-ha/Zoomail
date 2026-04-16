import os
from datetime import date

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods

from utils.file_response import file_response_or_404

from .models import Kansouyoushi


@login_required()
def index(request):
    kansou_qs = Kansouyoushi.objects.all().order_by("performed_at")

    # 各アイテムを年度毎にグループ化（performed_atが4月1日未満なら前年の年度とする）
    grouped = {}
    for item in kansou_qs:
        performed_date = item.performed_at
        group_year = performed_date.year
        if performed_date < date(performed_date.year, 4, 1):
            group_year -= 1

        grouped.setdefault(group_year, []).append(item)

    # 年度を降順にソートし、各年度内はperformed_atの降順に並べ替える
    sorted_years = sorted(grouped.keys(), reverse=True)
    result = []
    for year in sorted_years:
        items_sorted = sorted(grouped[year], key=lambda x: x.performed_at, reverse=True)
        items_list = []
        for item in items_sorted:
            file_size = item.file.size if item.file else ""
            items_list.append(
                {
                    "id": item.id,
                    "title": item.title,
                    "detail": item.detail,
                    "performed_at": item.performed_at,
                    "size": file_size,
                }
            )
        result.append(
            {
                "year": year,
                "items": items_list,
            }
        )

    return render(request, "kansou/index.html", {"kansou": result})


@require_http_methods(["GET"])
@login_required()
def download(request, kansou_id):
    kansou = get_object_or_404(klass=Kansouyoushi, id=kansou_id)
    extension = os.path.splitext(kansou.file.path)[-1]
    if kansou.detail:
        filename = f"{kansou.title} ({kansou.detail}){extension}"
    else:
        filename = f"{kansou.title}{extension}"
    return file_response_or_404(
        filepath=kansou.file.path,
        filename=filename,
        mimetype="application/pdf",
    )
