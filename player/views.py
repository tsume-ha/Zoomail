from django.shortcuts import render
from django.http import HttpResponse
from config import settings

def index(request):
	params = {
	
	}
	return render(request, 'player/index.html', params)

def playlist(request):
	params = {
	'media_url': settings.MEDIA_URL,
	}
	return render(request, 'player/playlist.html', params)