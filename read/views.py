from django.shortcuts import render
from django.http import HttpResponse
from .models import PostTest

def index(request):
	data = PostTest.objects.all().order_by('id').reverse() #逆順で取得
	params = {
		'search':'検索とかそういうの - 開発中',
		'data':data,
	}
	return render(request, 'read_index.html', params)

def content(request, cont_num):
	print(cont_num)
	data = PostTest.objects.all().filter(id=cont_num)
	params = {
		'data':data,
	}
	return render(request, 'read_content.html', params)