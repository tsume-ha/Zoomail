from django import template

register = template.Library()


@register.filter("make_message_short")
def make_message_short(content: str) -> str:
    text_max = 72  # 最大文字数
    if len(content) <= text_max:
        return content  # メッセージが短ければそのまま返す

    # 最初の改行を探す
    content = content.lstrip("\n")
    first_newline_index = content.find("\n")
    print(first_newline_index)
    if first_newline_index != -1:
        content = content[first_newline_index + 1 :]  # 最初の改行後の部分を切り取る

    # 文末の改行をすべて削除
    content = content.rstrip("\n")

    # すべての改行をスペースに変換
    content = content.replace("\n", " ")

    # 最終的な文字数チェックと短縮処理
    if len(content) > text_max:
        content = content[:text_max] + " ..."

    return content
