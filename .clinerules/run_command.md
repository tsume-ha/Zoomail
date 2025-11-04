Djangoアプリはdockerコンテナで動いているため`python manage.py ...`コマンドは

```
docker compose exec django python manage.py ...
```

の形で書くこと。
