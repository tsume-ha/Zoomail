# ベースイメージにNode.js 22 slimを使用
FROM node:22-slim

# 作業ディレクトリを指定
WORKDIR /app/scss

# sassをグローバルにインストール
RUN npm install -g sass@1.79.6

# コンテナ実行時のデフォルトコマンド
CMD ["sass", "custom.scss", "build/bootstrap-5-custom.css"]
