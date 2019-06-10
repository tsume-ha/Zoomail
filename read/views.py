from django.shortcuts import render
from django.http import HttpResponse

def index(request):
	params = {
		'search':'検索とかそういうの - 開発中',
	}
	return render(request, 'read/index.html', params)