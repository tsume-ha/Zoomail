from django.shortcuts import render
from django.http import HttpResponse

def index(request):
	params = {
	
	}
	return render(request, 'home/index.html', params)

def login(request):
	return render(request, 'admin/login.html')

def logout(request):
	return render(request, 'registration/logged_out.html')