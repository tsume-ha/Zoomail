from django import template
from django.utils.safestring import mark_safe
from player.models import Song

register = template.Library()


@register.simple_tag
def GetSongDetail(Performance):
    Songs = Song.objects.filter(performance=Performance).order_by('track_num')
    Performance_pk = Performance.pk
    text_return = '<p class="songdetail mt-4 mb-2">'
    for index, SongData in enumerate(Songs):
        text_return += '<span data-url="/player/playlist/' + str(Performance_pk) + '?track=' + str(index+1) + '" class="js-link">'
        text_return += str(SongData.track_num) + '. ' + SongData.song_name + '</span> '
    text_return += '</p><span class="p-0 pr-2 text-right small">ほか、全'
    text_return += str(len(Songs))
    text_return += '曲</span>'
    return mark_safe(text_return)

