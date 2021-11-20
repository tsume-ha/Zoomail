from utils.commom import download
import datetime

from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.http.response import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.forms import formset_factory, modelformset_factory
from django.utils.datastructures import MultiValueDictKeyError
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied

from .forms import CreateRehasalForm, EditSongForm
from .models import Live, Song
from config.permissions import RecordingPermisson


@login_required()
def index(request):
    lives = Live.objects.all().order_by('updated_at').reverse()
    return JsonResponse({
        "lives": [{
            "id": live.id,
            "date": live.recorded_at,
            "title": live.live_name,
            "songs": [{
                "id": sound.id,
                "trackNum": sound.track_num,
                "title": sound.song_name,
                "path": sound.file.url,
                "length": sound.length
              } for sound in live.songs.all()]
        } for live in lives]
    })


@login_required()
def content(request, id):
    live = get_object_or_404(Live, id=id)
    return JsonResponse({
        "id": live.id,
        "date": live.recorded_at,
        "title": live.live_name,
        "songs": [{
            "id": sound.id,
            "trackNum": sound.track_num,
            "title": sound.song_name,
            "path": sound.file.url,
            "length": sound.length
            } for sound in live.songs.all()
        ]
    })


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
        live, created = Live.objects.get_or_create(
            live_name=livename,
            recorded_at=recorded_at,
            updated_by=now_user,
        )
        content = songform.save(commit=False)
        content.live = live
        content.updated_by = now_user
        content.save()

        response = HttpResponse('OK')
        response.status_code = 200
        return response

    params = {
        'form': form,
    }
    return render(request, 'SPA.html', params)


@login_required()
def edit(request, live_id):
    now_user = request.user
    is_allowed = RecordingPermisson(now_user)
    if not is_allowed:
        raise PermissionDenied

    live = get_object_or_404(Live, id=live_id)
    FormSetExtraNum = 3
    EditSongFormSet = modelformset_factory(
        Song, EditSongForm, extra=FormSetExtraNum)
    formset = EditSongFormSet(
        request.POST or None, request.FILES or None,
        queryset=Song.objects.filter(
            live=live).order_by('track_num')
    )
    if request.method == 'POST':
        if formset.is_valid():
            instances = formset.save(commit=False)
            for instance in formset.deleted_objects:
                instance.delete()
            for instance in instances:
                instance.live = live
                instance.updated_by = now_user
                instance.updated_at = datetime.datetime.now()
                instance.save()
            return redirect('sound:playlist', live_id=live_id)
        else:
            print('validation error')
    params = {
        'live': live,
        'formset': formset,
    }
    return render(request, 'sound/edit.html', params)


@login_required()
def FileDownloadView(request, song_pk):
    try:
        song = Song.objects.get(pk=song_pk)
    except ObjectDoesNotExist:
        raise Http404
    filename = str(song.track_num).zfill(2) + ' ' + song.song_name + '.mp3'
    response = download(
        filepath=song.file.path,
        filename=filename,
        mimetype='audio/mpeg'
    )
    return response


@login_required()
def playlistJson(request, live_id):
    live = get_object_or_404(Live, id=live_id)
    songs = Song.objects.filter(live=live).order_by("track_num")
    return JsonResponse(
        {
            "live": {
                "id": live.id,
                "live_name": live.live_name,
                "recorded_at": live.recorded_at,
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
