from django.shortcuts import render
from django.http import HttpResponse

def index(request):
	params = {
	
	}
	return render(request, 'player/index.html', params)