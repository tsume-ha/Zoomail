from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter("URL_Tag_Property")
def URL_Tag_Property(content):
    content = content.replace('<a ', '<a target="_blank" rel="nofollow" class="text-break" ')
    return mark_safe(content)