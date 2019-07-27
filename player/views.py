from django.shortcuts import render
from django.http import HttpResponse
from config import settings

def index(request):
	params = {
	
	}
	return render(request, 'player/index.html', params)

def playlist(request):
	params = {
	'music_root': '/private-media/music',
	}
	return render(request, 'player/playlist.html', params)