from django.shortcuts import render

def index(request):
    params = {}
    return render(request, 'custom_admin/index.html', params)