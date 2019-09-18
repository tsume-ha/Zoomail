from django.shortcuts import render
from django.http import HttpResponse
from config import settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.forms import formset_factory
from django.utils.datastructures import MultiValueDictKeyError
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from .forms import CreateRehasalForm, CreateSongForm
from .models import Performance, Song
import datetime

def RecordingPermisson(user):
    return user.is_superuser or \
           user.groups.filter(name='RecordingGroup').exists()


@login_required()
def index(request):
    Performances = Performance.objects.all().order_by('updated_at').reverse()
    now_user = request.user
    is_allowed = RecordingPermisson(now_user)
    params = {
        'Performances': Performances,
        'is_allowed': is_allowed,
    }
    return render(request, 'player/index.html', params)


@login_required()
def playlist(request, live_id):
    Performances = get_object_or_404(Performance, id=live_id)
    Songs = Song.objects.filter(performance=Performances).order_by('track_num')
    params = {
    'Performances': Performances,
    'Songs': Songs,
    }
    if 'track' in request.GET:
        try:
            track = request.GET['track']
            if 0 < int(track):
                    SongToPreload = Songs.get(track_num=track)
                    params['SongToPreload'] = SongToPreload
        except :
            pass
    return render(request, 'player/playlist.html', params)

FormSetExtraNum = 20
CreateSongFormSet = formset_factory(CreateSongForm, extra=FormSetExtraNum)

@login_required()
def songupload(request):
    now_user = request.user
    is_allowed = RecordingPermisson(now_user)
    if is_allowed:
        params = {
            'CreateRehasalForm': CreateRehasalForm(),
            'CreateSongFormSet': CreateSongFormSet,
            }
        if (request.method == 'POST'):
            livename = request.POST["livename"]
            recorded_at = request.POST["recorded_at"]
            now_time = datetime.datetime.now()
            now_user = request.user
            content_Performance = Performance(
                live_name = livename,
                recorded_at = now_time,
                created_at = now_time,
                updated_at = now_time,
                updated_by = now_user
                )
            content_Performance.save()
            success_count = 0
            for i in range(FormSetExtraNum):
                try:
                    songname = "form-" + str(i) + "-song_name"
                    filename = "form-" + str(i) + "-song_file"
                    song_name = request.POST[songname]
                    song_file = request.FILES[filename]
                    content_Song = Song(
                        performance = content_Performance,
                        track_num = i + 1,
                        song_name = song_name,
                        file = song_file,
                        created_at = now_time,
                        updated_at = now_time,
                        updated_by = now_user
                    )
                    content_Song.save()
                    success_count += 1
                except MultiValueDictKeyError:
                    pass
            success_message = str(success_count) + '曲アップロードしました。'
            messages.success(request, success_message)
            return redirect('/player/playlist/' + str(content_Performance.id))
        return render(request, 'player/songupload.html', params)
    else:
        raise PermissionDenied



@login_required()
def download2(request):
    import os
    from io import BytesIO
    from config.settings import BASE_DIR
    import urllib.parse
    file = open(os.path.join(BASE_DIR, 'player', 'test2.mp3'), 'rb')
    response = HttpResponse(
        file,
        status=200, 
        content_type='audio/mp3',
        )
    filename = 'ほげほげ.mp3'
    response['Content-Disposition'] = 'attachment; filename="{fn}"'.format(fn=urllib.parse.quote(filename))
    return response