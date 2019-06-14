from django.shortcuts import render
from django.http import HttpResponse

def index(request):
	params = {
		'search':'検索とかそういうの - 開発中',
	}
	return render(request, 'read_index.html', params)

def content(request):
	params = {
		'tag':'全回メーリス',
		'article_body':'全回メーリス失礼します。会長の成です。※1回生のみなさんには関係のないメーリスです。読まなくても大丈夫です。6月ライブお疲れ様でした。本ライブのリハーサルでは制限時間、コメント内容の禁止事項など、いくつかルールを設けて、任意の形で口頭コメントを行いました。※ルールについては5/28の全回メーリス2911号をご覧ください。',
	}
	return render(request, 'read_content.html', params)