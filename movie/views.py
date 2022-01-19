from django.http.response import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.safestring import mark_safe
from django.utils.html import linebreaks, urlize

from .models import YoutubeURL

# html formatter
def target_blank(content):
    content = content.replace("<a ", '<a target="_blank" rel="nofollow ugc noopener" class="text-break" ')
    return mark_safe(content)


@login_required()
def index(request):
    items = YoutubeURL.objects.all().order_by("held_at").reverse()
    return JsonResponse(
        {
            "movies": [
                {
                    "id": item.id,
                    "title": item.title,
                    "description": target_blank(urlize(linebreaks(item.textcontent))),
                    "url": item.url,
                    "heldAt": item.held_at,
                }
                for item in items
            ]
        }
    )
