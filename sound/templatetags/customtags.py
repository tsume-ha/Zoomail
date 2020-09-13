from django import template
from django.utils.safestring import mark_safe

from sound.models import Song


register = template.Library()

@register.simple_tag
def GetSongDetail(live):
    Songs = Song.objects.filter(live=live).order_by('track_num')
    live_pk = live.pk
    text_return = '<p class="songdetail mt-4 mb-2">'
    for index, SongData in enumerate(Songs):
        text_return += '<span>'
        text_return += str(SongData.track_num) + '. ' + SongData.song_name + '</span> '
    text_return += '</p><span class="p-0 pr-2 text-right small">ほか、全'
    text_return += str(len(Songs))
    text_return += '曲</span>'
    return mark_safe(text_return)

@register.filter(name="seconds_to_time")
def seconds_to_MMSS(seconds):
    if seconds == 0:
        return ''
    else:
        minute = seconds // 60
        second = seconds % 60
        return str(minute).zfill(1) + ':' + str(second).zfill(2)
    