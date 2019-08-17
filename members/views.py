from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import Http404
from .models import User
from .forms import UserUpdateForm

@login_required(login_url='/login/')
def index(request):
	now_user = request.user
	#User.objects.get(now_user)
	params = {
		'user_pk': now_user.pk,
	}
	return render(request, 'members/index.html', params)

@login_required(login_url='/login/')
def Mypage(request, url_user_pk):
	now_user = request.user
	is_allowed = now_user.pk == url_user_pk or now_user.is_superuser
	if is_allowed:
		data = get_object_or_404(User,pk=url_user_pk)		
		params = {
			'data': data,
		}
		return render(request, 'members/mypage_detail.html', params)
	else:
		raise PermissionDenied

@login_required(login_url='/login/')
def UserUpdate(request, url_user_pk):
	now_user = request.user
	is_allowed = now_user.pk == url_user_pk or now_user.is_superuser
	if is_allowed:
		try:
			data = User.objects.get(pk=url_user_pk)
		except User.DoesNotExist:
			raise Http404
		
		if request.method == 'POST':
			pass

		else:
			params = {
				'form': UserUpdateForm(),
				'data': data,
			}
		return render(request, 'members/mypage_UserUpdate.html', params)
	else:
		raise PermissionDenied

from .create_google_user import Create_Google_User as register
from django.shortcuts import redirect

@login_required(login_url='/login/')
def UserRegistration(request):
	now_user = request.user
	is_allowed = now_user.is_superuser
	if is_allowed:
		register(email='hogehoge@example.com', year=2018)
		return redirect('/members')
	else:
		return redirect('/members')