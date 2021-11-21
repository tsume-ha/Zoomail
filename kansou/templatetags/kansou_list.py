from django import template
from django.utils.safestring import mark_safe
from kansou.models import Kansouyoushi
import datetime

register = template.Library()


@register.simple_tag
def GetKansouList(year):
    records = Kansouyoushi.objects.filter(performed_at__gte=datetime.date(year, 4, 1))\
                                  .filter(performed_at__lt=datetime.date(year + 1, 4, 1))\
                                  .order_by('performed_at').reverse()

    def readable_size(num, suffix='B'):
        for unit in ['','K','M','G','T']:
            if abs(num) < 1024.0:
                return "%3.1f%s%s" % (num, unit, suffix)
            num /= 1024.0
        return "%.1f%s%s" % (num, 'Yi', suffix)

    text_return = ''
    for record in records:
        text_return += '<a href="'
        text_return += record.file.url
        text_return += '" target="_blank" class="list-group-item list-group-item-action p-2"><h6 class="d-inline-block m-0">'
        text_return += record.title
        text_return += ' ('
        text_return += readable_size(record.file.size)
        text_return += ')</h6><span class="small m-2 p-1 pl-2 text-dark">'
        text_return += record.performed_at.strftime('%Y/%m/%d')
        text_return += '</span>'
        if record.detail != "":
            text_return += '<br><span class="small m-0 pl-2 text-dark">'
            text_return += record.detail
            text_return += '</span>'
        text_return += '</a>'
    return mark_safe(text_return)

