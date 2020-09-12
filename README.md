# UnpluggedMessage
Message board for Kyoto Univ. unplugged

## setting 
secret keyは、

~~setting_local.py に
  `SECRET_KEY = 'key_example'`
を打ち込んでこれを読み込み~~

`python3 manage.py migrate` でマイグレーションを実行
`python manage.py runserver` でローカルサーバー起動

本番サーバー上では、`manage.py`で動かすとき`--settings config.production`が必要。
例）`python3 manage.py migrate --settings config.production`
これがないとdefaultのsettings(sqlite3)にmigrateされる。


## webpack

webpack を導入しました.

生成物もgit管理下に置いているので, 動かすだけであれば設定不要です.

npm 6.14.4, node v13.13.0 をインストールしてください. 

`npm ci`