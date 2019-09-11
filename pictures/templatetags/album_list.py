from django import template
from django.utils.safestring import mark_safe
from pictures.models import Album
import datetime

register = template.Library()


@register.simple_tag
def GetAlbumList(year):
    records = Album.objects.filter(held_at__gte=datetime.date(year, 4, 1))\
                           .filter(held_at__lt=datetime.date(year + 1, 4, 1))\
                           .order_by('held_at').reverse()
    text_return = ''
    for record in records:
        text_return += '<div class="cardwrap col-6 col-xs-6 col-sm-6 col-md-4 col-lg-3 my-2"><article class="card"><img class="card-img-top" src="'
        if record.thumbnail:
            text_return += record.thumbnail.url
        else:
            text_return += '/static/img/album_thum_default.jpg'
        text_return += '"><a href="'
        text_return += record.url
        text_return += '" class="card-img-overlay" target="_blank"><h5 class="card-title">'
        text_return += record.title
        text_return += '</h5><h6 class="card-subtitle">'
        text_return += record.held_at.strftime('%Y/%m/%d')
        text_return += '</h6></a></article></div>'

    return mark_safe(text_return)

