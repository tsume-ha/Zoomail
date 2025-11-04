# 開発環境の立ち上げ

## DBのmigration

ZoomailではカスタムしたUserテーブルを作成している。
Adminなどのテーブルのmigration前にUserテーブルをmigrateしなければならないので、
先に干渉するappを止めてからmigrationを行う。

migrationする前に`django.contrib.admin`と`social_django`の登録をコメントアウトする。

```python config/settings.py
INSTALLED_APPS = [
    #"django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    #"social_django",
    "top",
    "members",
]
```

また、これを使う`urls.py`もコメントアウトする
```python config.urls.py
urlpatterns = [
    # path("admin/", admin.site.urls),
    path("auth/", include("social_django.urls", namespace="social")),
]
```

この状態で、先に`members`のテーブルだけをmigrateする。
```bash
python manage.py migrate members
```

この後に、先ほどのコメントアウトを外し、全体をmigrateする。
```bash
python manage.py migrate
```

