from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def GetKansouList(year):

    return mark_safe(text_return)

