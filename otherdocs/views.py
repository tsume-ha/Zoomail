from django.http.response import JsonResponse
from django.http import FileResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.template.defaultfilters import filesizeformat

from .models import Content


@login_required()
def index(request):
    contents = Content.objects.all().order_by(
        "-index",
        "-updated_at"
        # index大きい順, updated_at新しい順
    )
    return JsonResponse(
        {
            "contents": [
                {
                    "id": content.id,
                    "title": content.title,
                    "updatedAt": content.updated_at,
                    "detail": content.detail,
                    "size": filesizeformat(content.file.size),
                }
                for content in contents
            ]
        }
    )


@login_required()
def ContentDownloadView(request, content_id):
    content = get_object_or_404(Content, id=content_id)
    filename = content.title + content.extension()
    return FileResponse(open(content.file.path, "rb"), as_attachment=False, filename=filename)
