from django import template
from django.utils.safestring import mark_safe
from board.models import Kidoku, Bookmark
import datetime
from django.contrib.staticfiles.templatetags.staticfiles import static

register = template.Library()


@register.filter("MakeMessageShort")
def MakeMessageShort(content):
    textmax = 80
    # メッセージが短いとき
    if len(content) < textmax:
        return content
    # 最初の改行を認識
    count = content.find('\n')
    # 文末の改行を削除
    while content[-2:-1] == '\n':
        content = content[:-3]
    # すべての改行をスペースに変換
    content = content[count:].replace('\n', ' ')
    
    if len(content) < textmax + 5:
        return content
    content = content[:textmax] + ' ...'
    return content

@register.simple_tag
def is_updated(message):
    text_return = ''
    if message.created_at + datetime.timedelta(seconds=5) < message.updated_at:
        text_return += '<span class="updated float-left alert-warning small p-1">'
        text_return += message.updated_at.strftime('%Y/%m/%d %H:%M')
        text_return += ' 更新</span>'
    return mark_safe(text_return)

@register.simple_tag
def no_kidoku_css_class(message, user):
    if not Kidoku.objects.filter(message=message).filter(user=user).exists():
        return " midoku"
    else:
        return ''

@register.simple_tag
def is_marked(message, user):
    if Bookmark.objects.filter(message=message).filter(user=user).exists():
        return static('img/star_yl.png')
    else:
        return static('img/star_bk.png')

@register.filter("AddTarget_blank")
def AddTarget_blank(content):
    content = content.replace('<a ', '<a target="_blank" rel="nofollow ugc noopener" class="text-break" ')
    return mark_safe(content)