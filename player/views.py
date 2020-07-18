from utils.commom import download
import datetime

from django.shortcuts import render
from django.http import HttpResponse
from django.http.response import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.forms import formset_factory, modelformset_factory
from django.utils.datastructures import MultiValueDictKeyError
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied

from .forms import CreateRehasalForm, EditSongForm
from .models import Performance, Song
from config.permissions import RecordingPermisson


@login_required()
def index(request):
    performances = Performance.objects.all().order_by('updated_at').reverse()
    now_user = request.user
    is_allowed = RecordingPermisson(now_user)
    params = {
        'performances': performances,
        'is_allowed': is_allowed,
    }
    return render(request, 'player/index.html', params)


@login_required()
def playlist(request, live_id):
    performance = get_object_or_404(Performance, id=live_id)
    params = {
        'performance': performance,
    }
    return render(request, 'player/playlist.html', params)


@login_required()
def upload(request):
    now_user = request.user
    is_allowed = RecordingPermisson(now_user)
    if not is_allowed:
        raise PermissionDenied
    form = CreateRehasalForm(request.POST or None)
    if (request.method == 'POST'):
        songform = EditSongForm(request.POST, request.FILES)
        if not (form.is_valid() and songform.is_valid()):
            response = HttpResponse('BAD REQUEST')
            response.status_code = 400
            return response

        livename = form.cleaned_data['livename']
        recorded_at = form.cleaned_data['recorded_at']
        performance, created = Performance.objects.get_or_create(
            live_name=livename,
            recorded_at=recorded_at,
            updated_by=now_user,
        )
        content = songform.save(commit=False)
        content.performance = performance
        content.updated_by = now_user
        content.save()

        response = HttpResponse('OK')
        response.status_code = 200
        return response

    params = {
        'form': form,
    }
    return render(request, 'player/upload.html', params)


@login_required()
def edit(request, live_id):
    now_user = request.user
    is_allowed = RecordingPermisson(now_user)
    if not is_allowed:
        raise PermissionDenied

    performance = get_object_or_404(Performance, id=live_id)
    FormSetExtraNum = 3
    EditSongFormSet = modelformset_factory(
        Song, EditSongForm, extra=FormSetExtraNum)
    formset = EditSongFormSet(
        request.POST or None, request.FILES or None,
        queryset=Song.objects.filter(
            performance=performance).order_by('track_num')
    )
    if request.method == 'POST':
        if formset.is_valid():
            instances = formset.save(commit=False)
            for instance in formset.deleted_objects:
                instance.delete()
            for instance in instances:
                instance.updated_by = now_user
                instance.updated_at = datetime.datetime.now()
                instance.save()
            return redirect('player:playlist', live_id=live_id)
        else:
            print('validation error')
    params = {
        'performance': performance,
        'formset': formset,
    }
    return render(request, 'player/edit.html', params)


@login_required()
def FileDownloadView(request, live_id, song_pk):
    try:
        song = Song.objects.get(pk=song_pk)
    except ObjectDoesNotExist:
        return redirect('/player/playlist/' + str(live_id))
    filename = str(song.track_num).zfill(2) + ' ' + song.song_name + '.mp3'
    print(song.file.path)
    response = download(
        filepath=song.file.path,
        filename=filename,
        mimetype='audio/mpeg'
    )
    return response


@login_required()
def GetSongData(request, live_id):
    performance = get_object_or_404(Performance, id=live_id)
    songs = Song.objects.filter(performance=performance).order_by("track_num")
    return JsonResponse(
        {
            "performance": {
                "id": performance.id,
                "live_name": performance.live_name,
                "recorded_at": performance.recorded_at,
            },
            "songs": [
                {
                    "id": song.id,
                    "track_num": song.track_num,
                    "song_name": song.song_name,
                    "fileurl": song.file.url,
                    "length": song.length,
                }
            for song in songs],
        }
    )
