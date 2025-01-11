# 開発環境の設定
FROM python:3.12-bookworm AS develop

WORKDIR /django

# 環境変数を設定
ENV PYTHONDONTWRITEBYTECODE=1 \
    # Pythonがpyc filesとdiscへ書き込むことを防ぐ
    PYTHONUNBUFFERED=1 \
    # Pythonが標準入出力をバッファリングすることを防ぐ
    PIP_DISABLE_PIP_VERSION_CHECK=on
# pip の定期的なバージョンチェックを無効化する

# パッケージ更新
RUN apt-get update --fix-missing && apt upgrade -y

# pythonパッケージのインストール
RUN pip install --upgrade pip
RUN pip install uWSGI==2.0.28

# ホストのカレントディレクトリ（現在はdjangoディレクトリ）を作業ディレクトリにコピー
COPY requirements.txt /django/requirements.txt

# requirementsからパッケージをインストールしてDjango環境を構築
RUN pip install -r requirements.txt


FROM python:3.12-slim-bookworm AS production
# 実行環境の設定

WORKDIR /django

# Pythonがpyc filesとdiscへ書き込むことを防ぐ
ENV PYTHONDONTWRITEBYTECODE=1 \
    # Pythonが標準入出力をバッファリングすることを防ぐ
    PYTHONUNBUFFERED=1 \
    # pip の定期的なバージョンチェックを無効化する
    PIP_DISABLE_PIP_VERSION_CHECK=on

# パッケージ更新
RUN apt-get update --fix-missing && apt upgrade -y

# パッケージのコピー
COPY --from=develop /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=develop /usr/local/bin/uwsgi /usr/local/bin/uwsgi
COPY --from=develop /usr/lib /usr/lib

# ソースコードのコピー
COPY . /django/
