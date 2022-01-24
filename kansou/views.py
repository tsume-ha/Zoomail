from django.http.response import JsonResponse
from django.http import FileResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.template.defaultfilters import filesizeformat
from .models import Kansouyoushi


@login_required()
def index(request):
    records = Kansouyoushi.objects.all().order_by("performed_at")
    return JsonResponse(
        {
            "kansou": [
                {
                    "id": item.id,
                    "title": item.title,
                    "detail": item.detail,
                    "url": item.file.url,
                    "performedAt": item.performed_at,
                    "size": filesizeformat(item.file.size),
                }
                for item in records
            ]
        }
    )


@login_required()
def kansouDownloadView(request, kansou_id):
    kansou = get_object_or_404(klass=Kansouyoushi, id=kansou_id)
    filename = ""
    if kansou.detail:
        filename = "{} ({}) .pdf".format(kansou.title, kansou.detail)
    else:
        filename = "{}.pdf".format(kansou.title)
    return FileResponse(open(kansou.file.path, "rb"), as_attachment=False, filename=filename)
