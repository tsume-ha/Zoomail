from django import template
import datetime

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

