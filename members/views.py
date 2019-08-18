from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.http import Http404
from .models import User, TmpMember
from .forms import UserUpdateForm
import csv
from io import TextIOWrapper

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
from .forms import RegisterForm, RegisterCSV, DivErrorList

@login_required(login_url='/login/')
def UserRegistration(request):
    now_user = request.user
    is_allowed = now_user.is_superuser
    if is_allowed:
        form = RegisterForm(request.POST or None)
        params = {
            'RegisterForm': form,
        }
        if (request.method == 'POST'):
            if form.is_valid():
                email = request.POST["email"]
                year = request.POST["year"]
                last_name = request.POST["last_name"]
                first_name = request.POST["first_name"]
                furigana = request.POST["furigana"]
                register(email=email, year=year, last_name=last_name, first_name=first_name)
                messages.success(request, email + 'を登録しました。')
            else:
                messages.error(request, '登録に失敗しました。')
                params['RegisterForm'] = RegisterForm(None)
        return render(request, 'members/register.html', params)
    else:
        return redirect('/members')


@login_required(login_url='/login/')
def UserRegistrationCSV(request):
    now_user = request.user
    is_allowed = now_user.is_superuser
    if is_allowed:
        csvform = RegisterCSV(request.POST or None, request.FILES or None, error_class=DivErrorList)
        params = {
            'RegisterCSV': csvform,
        }
        if (request.method == 'POST'):
            form_data = TextIOWrapper(request.FILES['csv_file'].file, encoding='utf_8')
            reader = csv.reader(form_data)
            session = request.session.session_key
            for row in reader:
                content = TmpMember(
                    session = session,
                    last_name = row[0],
                    first_name = row[1],
                    furigana = row[2],
                    email = row[3],
                    year = int(row[4]),
                    )
                content.save()
            return redirect('preview/')
                # print(row)['2019/08/18 0:02:36', '橋爪', '雅史', 'はしづめまさふみ', 'hashimasa0503@gmail.com', '24']


            # if csvform.is_valid():
            #     csv = 
            #     print(csv)
            #     params['confirm'] = True
            # else:
            #     messages.error(request, '登録に失敗しました。')
        return render(request, 'members/registerCSV.html', params)
    else:
        return redirect('/members')

@login_required(login_url='/login/')
def UserRegistrationPreview(request):
    now_user = request.user
    is_allowed = now_user.is_superuser
    if is_allowed:
        TmpMembers = TmpMember.objects.filter(session=request.session.session_key).order_by('id')
        aboid_delete_data = TmpMembers
        params = {
            'TmpMembers': aboid_delete_data
        }
        if (request.method == 'POST'):
            MembersToRegister = aboid_delete_data
            for member in MembersToRegister:
            	register(email=member.email, year=member.year, last_name=member.last_name, first_name=member.first_name)
            messages.success(request, '登録しました')
            TmpMembers.delete()
            return redirect('/members/register/csv/')
        return render(request, 'members/register_preview.html', params)
    else:
        return redirect('/members')