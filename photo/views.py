from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import PhotoAlbum


@login_required()
def index(request):
    items = PhotoAlbum.objects.all().order_by("held_at").reverse()
    return render(request, "photo/index.html", {"items": items})
