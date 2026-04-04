# 開発環境の立ち上げ

## 本番サーバーでの起動方法

このリポジトリの production 構成は、以下の前提で動かします。

- ホストの nginx が `collected_static` を直接配信する
- Docker コンテナ内の Django / gunicorn は 8000 番で待ち受ける
- `compose.prod.yaml` では `./collected_static` と `./private_media` を bind mount する
- Django コンテナは `APP_UID` / `APP_GID` で作成した `zoomail` ユーザーで動く

そのため、**本番サーバーでは bind mount 先ディレクトリを事前に、デプロイ実行ユーザーと同じ UID/GID で作成しておく必要があります。**
ここがずれていると `python manage.py collectstatic` 実行時に `PermissionError` になります。

### 1. 初回セットアップ

本番サーバーで deploy を実行するユーザーで `/srv/zoomail` に配置されている前提です。

```bash
cd /srv/zoomail
id -u
id -g
mkdir -p collected_static private_media
```

`id -u` と `id -g` の結果を `.env` に設定します。

```dotenv
APP_UID=1000
APP_GID=1000
```

`APP_UID` / `APP_GID` には、**実際に deploy を実行するユーザーの UID/GID** を設定してください。

bind mount 先の所有者・権限を確認します。

```bash
stat -c '%A %U:%G %u:%g %n' collected_static private_media
test -w collected_static
test -w private_media
```

少なくとも、deploy 実行ユーザーから `collected_static` と `private_media` に書き込みできる必要があります。

### 2. 起動

```bash
cd /srv/zoomail
git pull
mkdir -p collected_static private_media
docker compose -f compose.prod.yaml down
docker compose -f compose.prod.yaml up --build -d
```

`entrypoint.prod.sh` で以下が順に実行されます。

1. `collectstatic`
2. `migrate`
3. `gunicorn --bind 0.0.0.0:8000`

ホスト nginx は `collected_static` を直接配信し、動的リクエストだけを `127.0.0.1:8000` にリバースプロキシする想定です。

### 3. 権限エラーが出たときの確認

`collectstatic` で `PermissionError: [Errno 13] Permission denied` が出る場合は、まず以下を確認してください。

```bash
cd /srv/zoomail
grep -E '^(APP_UID|APP_GID)=' .env
stat -c '%A %U:%G %u:%g %n' collected_static private_media
```

`.env` の `APP_UID` / `APP_GID` と、`collected_static` / `private_media` の実所有者が一致していないと、
コンテナ内の `zoomail` ユーザーが bind mount 先に書き込めず起動に失敗します。

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

## Python依存パッケージの更新手順

Zoomail では、`requirements.txt` を **最終的に `pip freeze` の結果で固定** して管理します。
Dependabot で直接依存・間接依存の両方を追跡しやすくするためです。

更新するときは、次の流れで行います。

1. まず `requirements.txt` を、アプリが直接使う最小限の依存だけにする
2. development コンテナを build して依存関係を解決する
3. コンテナ内で `pip freeze` を実行し、結果で `requirements.txt` を更新する
4. Django の最低限の起動確認を行う

### 最小依存から再生成するときの例

`requirements.txt` を直接依存だけにしたあと、以下を実行します。

```bash
docker compose run --rm --build django pip freeze
```

出力された内容で `requirements.txt` を更新したら、Django コンテナを起動して確認します。

```bash
docker compose up -d django
docker compose exec django python manage.py check
```

### 間接依存に脆弱性が見つかったとき

Dependabot で脆弱性警告が出た場合は、次の順で対処します。

1. まず、どの **直接依存** が問題の **間接依存** を引き込んでいるか確認する
2. 可能なら、親になっている直接依存を更新して解消する
3. 親の更新だけで解消しない場合は、互換性を確認したうえで、必要なバージョンが入るように最小依存の見直しを行う
4. その状態で development コンテナを再 build する
5. `pip freeze` を取り直して `requirements.txt` を更新する
6. 最後に `docker compose exec django python manage.py check` などで最低限の動作確認を行う

重要なのは、**間接依存だけを場当たり的に手で直すのではなく、最終的に再度 `pip freeze` して `requirements.txt` 全体を実環境と一致させること** です。

## バックアップしたDBダンプをローカルの Docker MariaDB にリストアする

`backup.sh` では、以下の形式で DB バックアップを作成しています。

- `mariadb-dump --databases "$DATABASE_NAME"` で **アプリ用データベースだけ** を SQL ダンプする
- その SQL ファイルを `tar.gz` に固める
- 例: `zoomail_20260404_1508.tar.gz`

この方式では、**本番環境と開発環境で異なる DB パスワードを使用できます。**
リストア時に使用するのは、**ローカル Docker MariaDB 側の接続情報**です。

また、`mysql` システム DB やユーザー権限テーブルを含めないため、
**開発環境ではローカル用の DB ユーザー/パスワードを維持したまま、アプリケーションデータだけを復元**できます。

### 注意

以下の手順には `docker compose down -v` が含まれます。これは、**ローカルの MariaDB volume を削除し、現在のローカル DB データを完全に消す操作**です。

必要なデータが残っていないことを確認してから実行してください。

### 手順

1. バックアップファイルをプロジェクトルートに置く

   例:

   ```bash
   ls zoomail_20260404_1508.tar.gz
   ```

2. 必要なら既存のローカル DB を削除する

   ```bash
   docker compose down -v
   ```

   ローカル DB を完全に入れ替える場合に実行します。
   volume を削除したくない場合は、この手順を省略できます。

3. DB コンテナだけ先に起動する

   ```bash
   docker compose up -d database
   ```

4. ローカル DB に接続できることを確認する

   ```bash
   docker compose exec database sh -lc 'exec mariadb -uroot -p"$MARIADB_ROOT_PASSWORD" -e "SELECT 1;"'
   ```

   このコマンドでは、**DB コンテナ内に設定されている `MARIADB_ROOT_PASSWORD`** を使用しています。
   本番環境の DB パスワードと一致している必要はありません。

   なお、`docker compose exec ... mariadb -p"$DATABASE_PASSWORD"` のようにホスト側で `$DATABASE_PASSWORD` を展開する書き方は、
   実行シェルに変数が設定されていない場合に空文字として扱われることがあるため、README では採用していません。

5. `tar.gz` の中の SQL をそのまま MariaDB に流し込む

   ```bash
   tar -xOf zoomail_20260404_1508.tar.gz | docker compose exec -T database sh -lc 'exec mariadb -uroot -p"$MARIADB_ROOT_PASSWORD"'
   ```

   - `tar -xOf ...` でアーカイブ内の SQL を標準出力に展開しています
   - `docker compose exec -T database ...` で DB コンテナに標準入力を渡しています
   - ダンプは `--databases "$DATABASE_NAME"` で作られているため、`CREATE DATABASE` / `USE` を含んだ SQL をそのまま流し込めます

6. 必要ならアプリ全体を起動する

   ```bash
   docker compose up -d
   ```

7. 接続確認をする

   ```bash
   docker compose exec database sh -lc 'exec mariadb -uroot -p"$MARIADB_ROOT_PASSWORD" -e "SHOW DATABASES;"'
   ```

### 補足

- 開発用 `compose.yaml` の DB サービス名は `database` です
- root パスワードは `.env` の `DATABASE_PASSWORD` がコンテナ内に渡されます
- リストア時に必要なのは **ローカル環境の root パスワード** であり、本番環境の DB パスワードではありません
- README のコマンドは、ホスト側の環境変数展開に依存しないよう **コンテナ内の `MARIADB_ROOT_PASSWORD` を使う形** にしています
- 既存の `--all-databases` ダンプには `mysql` システム DB が含まれる可能性があります。開発環境のユーザー/権限を維持する運用では、**アプリ DB 単体のダンプを使用する**のが適しています


