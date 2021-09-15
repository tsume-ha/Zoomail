# Zoomail (旧UnpluggedMessage)
[https://message.ku-unplugged.net/](https://message.ku-unplugged.net/)

京大アンプラグドの部内連絡用ウェブサイト



## Setting

### 全体設定

    $ git clone
    $ cd UnpluggedMessage
    $ pip install -r requirements.txt

`config/base.env` に`SECRET_KEY`, `SOCIAL_AUTH_GOOGLE_OAUTH2_KEY`, `SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET`を記述

Djangoの設定

    $ python manage.py migrate
    $ python manage.py runserver 3333

ローカルサーバーが起動していることを確認
[localhost:3333](localhost:3333)

ctrl + C でサーバー停止

Superuserの登録

    $ python manage.py createsuperuser

Emailアドレスとして有効なGmailアドレスを入力
Googleにログインできるものでないと不可
パスワードは使わないのでなんでも

#### Google Oauth の設定
工事中

ログイン

    $ python manage.py runserver 3333

ローカルサーバーからログイン
[localhost:3333](localhost:3333)


#### Sendgridの設定
工事中

#### Google Calendar APIの設定
工事中

#### 本番環境でのデプロイ

本番サーバー上では、`manage.py`で動かすとき`--settings config.production`が必要。

    $ python3 manage.py migrate --settings config.production

`production`のオプションを付けないと、migrateされるデータベース先が異なり、defaultのsqliteに
migrateされてしまう


## webpack

webpack を導入しました.

生成物もgit管理下に置いているので, 動かすだけであれば設定不要です.

npm 6.14.4, node v13.13.0 をインストールしてください. 

`npm ci`

### webpack移行中
フロント部分をvue3に移行中です



## 例会教室API
- 当日分のみ：`https://message.ku-unplugged.net/api/meeting_room/today/`
- 1か月分：`https://message.ku-unplugged.net/api/meeting_room/get31day/`

アクセスするとJson返します

