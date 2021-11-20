from django.http.response import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Album

@login_required()
def index(reqest):
    return JsonResponse({
        "photos": [{
            "id": photo.id,
            "title": photo.title,
            "date": photo.held_at.strftime("%Y-%m-%d"),
            "url": photo.url,
            "thumbnail": photo.thumbnail.url if photo.thumbnail else None
        } for photo in Album.objects.all().order_by('held_at')]
    })