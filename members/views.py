from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.http import Http404
from .models import User, TmpMember
from social_django.models import UserSocialAuth
from .forms import UserUpdateForm, RegisterForm, RegisterCSV
import csv
from io import TextIOWrapper
from .create_google_user import DuplicateGmailAccountError
from board.models import Message
from .create_google_user import Create_Google_User as register


def MemberRegisterPermission(user):
    return user.is_superuser or\
        user.groups.filter(name='Administer').exists()

@login_required()
def index(request):
    now_user = request.user
    register_allowed = MemberRegisterPermission(now_user)
    messages_you_send = Message.objects.filter(sender=now_user)
    messages_you_wrote = Message.objects.filter(writer=now_user).exclude(sender=now_user)
    params = {
        'register_allowed': register_allowed,
        'yousend': messages_you_send,
        'yourmessage_otherssend': messages_you_wrote,
    }
    return render(request, 'members/index.html', params)

@login_required()
def UserUpdate(request):
    now_user = request.user
    form = UserUpdateForm(request.POST or None, instance=now_user)
    if (request.method == 'POST'):
        if form.is_valid():
            content = form
            content.save()
            messages.success(request, '更新しました')
            return redirect('/members')
        else:
            messages.error(request, '更新できませんでした')
    params = {
        'form': form,
    }
    return render(request, 'members/mypage_UserUpdate.html', params)

@login_required()
def UserRegistration(request):
    now_user = request.user
    is_allowed = MemberRegisterPermission(now_user)
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
                register(email=email, year=int(year), last_name=last_name, first_name=first_name, furigana=furigana)
                messages.success(request, email + 'を登録しました。')
            else:
                messages.error(request, '登録に失敗しました。')
                params['RegisterForm'] = RegisterForm(None)
        return render(request, 'members/register.html', params)
    else:
        return redirect('/members')


@login_required()
def UserRegistrationCSV(request):
    now_user = request.user
    is_allowed = MemberRegisterPermission(now_user)
    if is_allowed:
        csvform = RegisterCSV(request.POST or None, request.FILES or None)
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
        return render(request, 'members/registerCSV.html', params)
    else:
        return redirect('/members')

@login_required()
def UserRegistrationPreview(request):
    now_user = request.user
    is_allowed = MemberRegisterPermission(now_user)
    if is_allowed:
        TmpMembers = TmpMember.objects.filter(session=request.session.session_key).order_by('id')
        params = {
            'TmpMembers': TmpMembers
        }
        if (request.method == 'POST'):
            MembersToRegister = TmpMembers
            is_error = False
            for member in MembersToRegister:
                try:
                    register(email=member.email, year=member.year, last_name=member.last_name, first_name=member.first_name)
                    member.delete()
                except DuplicateGmailAccountError:
                    messages.error(request, member.email+' はすでに登録されているアカウントのため登録できませんでした。')
                    is_error = True
            if is_error:
                messages.error(request, '一部ユーザーが登録できませんでした。登録できなかったユーザーが以下の表に残されています。')
                return render(request, 'members/register_preview.html', params)
            else:
                messages.success(request, '登録しました')
                return redirect('/members/register/csv/')
        return render(request, 'members/register_preview.html', params)
    else:
        return redirect('/members')