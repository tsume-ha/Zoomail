from movie.models import YoutubeURL
from members.models import User

# ユーザーIDを指定
user_id = 1  # 実際のユーザーIDに置き換えてください

# 新しいレコードの作成
new_youtube_url = YoutubeURL(
    title="2019 新人ライブ",
    url="https://www.youtube.com/embed?listType=playlist&list=PLnef8kmQPUwXoWLE_V74Zdipz-PUGfvfn&rel=0",
    textcontent="",  # 必要に応じて内容を追加
    held_at="2019-06-28",
    created_by=User.objects.get(id=user_id),  # ユーザーを取得
)
new_youtube_url.save()  # データベースに保存
