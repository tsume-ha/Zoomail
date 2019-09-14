from django.shortcuts import render, redirect
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Max, Min, Count
from .models import Album
from .forms import AlbumRegisterForm
import datetime
from imagekit import ImageSpec
from imagekit.processors import ResizeToFill
from django.utils.datastructures import MultiValueDictKeyError


class Thumbnail(ImageSpec):
    processors = [ResizeToFill(400, 300)]
    format = 'JPEG'
    options = {'quality': 60}



def PicturesPermission(user):
    return user.is_superuser or\
           user.groups.filter(name='Administer').exists()

def exist_years(records):
    if records.exists():
        # レコードが登録されている「年度」の範囲のリストを返します
        data_min = records.aggregate(Min('held_at'))['held_at__min']
        data_max = records.aggregate(Max('held_at'))['held_at__max']
        year_list = []
        for year in range(data_min.year - 1, data_max.year + 1):
            is_exist = records.filter(held_at__gte=datetime.date(year, 4, 1),\
                                      held_at__lt=datetime.date(year + 1, 4, 1)).exists()
            if is_exist:
                year_list.append(year)
        year_list.sort(reverse=True)
        return year_list
    else:
        return []

@login_required()
def index(request):
    records = Album.objects.all()

    params = {
        'pictures_allowed': PicturesPermission(user=request.user),
        'exist_years': exist_years(records)
    }
    return render(request, 'pictures/index.html', params)

@login_required()
def PhotoRegister(request):
    now_user = request.user
    is_allowed = PicturesPermission(user=request.user)
    if is_allowed:
        form = AlbumRegisterForm(request.POST or None, request.FILES or None)
        params = {
            'form': form,
        }
        if (request.method == 'POST'):
            if form.is_valid():
                content = form.save(commit=False)
                try:
                    thum = request.FILES["thumbnail"]
                    source_file = open(thum.temporary_file_path(), 'rb')
                    image_generator = Thumbnail(source=source_file)
                    result = image_generator.generate()
                    dest = open(thum.temporary_file_path(), 'wb')
                    dest.write(result.read())
                    dest.close()
                except MultiValueDictKeyError:
                    pass
                content.created_by = now_user
                content.save()
                messages.success(request, '登録しました。')
                return redirect('/pictures/')
            else:
                messages.error(request, '登録できませんでした。')
        return render(request, 'pictures/register.html', params)
    else:
        return redirect('/pictures/')