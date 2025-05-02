# マルチステージDockerfile(node.jsでビルド してから nginxでビルド結果を配信)
# slim系のnodeから構築することを定義(22は比較的新しくてLTSなので採用)
FROM node:22.14.0-bullseye-slim AS builder
# Docker イメージをビルドする時の、コンテナ内作業ディレクトリを /app に設定
# このディレクトリを基準にして、この後のRUNやCOPYが実行される。
WORKDIR /app
# build-time ARG の定義
ARG VITE_API_BASE_URL
ENV VITE_API_BASE_URL=$VITE_API_BASE_URL
# ENV VITE_API_BASE_URL=abc

# npmパッケージのインストール開始
COPY frontend/package*.json ./
RUN npm install
# vue.jsのビルド開始
COPY frontend/ ./
RUN npm run build
#---ここまでが、node.jsイメージでのステージ(ビルド用) --　ここからはnginxでの動作---
# nginxでの配信用ステージ（最終イメージ）
FROM nginx:latest
# マルチステージビルドの1つめ(=AS builderとしたFROM部分)で作成されたコンテナの/app/distディレクトリ内のものをnginxコンテナの配信ディレクトリへコピー
COPY --from=builder /app/dist /usr/share/nginx/html

# Nginx 設定カスタマイズが必要なら:
COPY front_nginx/nginx_confs/development/nginx.conf /etc/nginx/nginx.conf

# このDockerfileとdevelopment.ymlを使う場合、docker-compose -f development.yml up --buildでいい
# 実行後は、http://localhost:8080でビルド後の結果を配信できる