from django import template
from django.utils.safestring import mark_safe

from board.models import Bookmark, Attachment

register = template.Library()

@register.simple_tag
def is_bookmarked(message, user):
    result = Bookmark.objects.filter(message=message).filter(user=user).exists()
    return str(result).lower()

# @register.simple_tag
# def attachments_url(message):
#     query = Attachment.objects.filter(message=message)
#     result = []
#     for item in query:
#         result += str(item.)
#     return result

@register.filter("target_blank")
def target_blank(content):
    content = content.replace('<a ', '<a target="_blank" rel="nofollow ugc noopener" class="text-break" ')
    return mark_safe(content)

