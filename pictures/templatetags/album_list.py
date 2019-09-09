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
        text_return += '<a href="'
        text_return += record.url
        text_return += '" target="_blank" class="list-group-item list-group-item-action p-2"><h6 class="d-inline-block text-primary m-0">'
        text_return += record.title
        text_return += '</h6><span class="small m-2 p-1 pl-2 text-dark">'
        text_return += record.held_at.strftime('%Y/%m/%d')
        text_return += '</span>'
        if record.detail != "":
            text_return += '<br><span class="small m-0 pl-2 text-dark">'
            text_return += record.detail
            text_return += '</span>'
        text_return += '</a>'
    return mark_safe(text_return)

