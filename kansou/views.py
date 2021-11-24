from django.http.response import JsonResponse
from django.contrib.auth.decorators import login_required

from .models import Kansouyoushi


@login_required()
def index(request):
    records = Kansouyoushi.objects.all().order_by("performed_at")
    return JsonResponse({
        "kansou": [{
            "id": item.id,
            "title": item.title,
            "detail": item.detail,
            "url": item.file.url,
            "performedAt": item.performed_at
        } for item in records]
    })

