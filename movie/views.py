from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import YoutubeURL

@login_required()
def index(request):
    data = YoutubeURL.objects.all().order_by('held_at').reverse()
    params = {
    'movies': data,
    }
    return render(request, 'movie/index.html', params)