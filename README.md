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
