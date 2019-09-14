from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Kansouyoushi
from .forms import KansouUploadForm
from django.db.models import Max, Min, Count
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib import messages
import datetime

def KansouPermission(user):
    return user.is_superuser or\
           user.groups.filter(name='Administer').exists()

def exist_years(records):
    if records.exists():
        # レコードが登録されている「年度」の範囲のリストを返します
        data_min = records.aggregate(Min('performed_at'))['performed_at__min']
        data_max = records.aggregate(Max('performed_at'))['performed_at__max']
        year_list = []
        for year in range(data_min.year - 1, data_max.year + 1):
            is_exist = records.filter(performed_at__gte=datetime.date(year, 4, 1),\
                                      performed_at__lt=datetime.date(year + 1, 4, 1)).exists()
            if is_exist:
                year_list.append(year)
        year_list.sort(reverse=True)
        return year_list
    else:
        return []

@login_required()
def index(request):
    records = Kansouyoushi.objects.all()

    params = {
        'kansou_allowed': KansouPermission(user=request.user),
        'exist_years': exist_years(records)
    }
    return render(request, 'kansou/index.html', params)


@login_required()
def KansouUpload(request):
    now_user = request.user
    is_allowed = KansouPermission(now_user)
    if is_allowed:
        form = KansouUploadForm(request.POST or None, request.FILES or None)
        params = {
            'form': form,
        }
        if (request.method == 'POST'):
            if form.is_valid():
                form.save(commit=False)
                form.created_by = now_user
                form.save()
                messages.success(request, '登録しました。')
                return redirect('/kansou/')
            else:
                messages.error(request, '登録できませんでした。')
        return render(request, 'kansou/upload.html', params)
    else:
        return redirect('/kansou/')