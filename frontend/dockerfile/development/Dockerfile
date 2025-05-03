# マルチステージDockerfile(node.jsでビルド してから nginxでビルド結果を配信)
# slim系のnodeから構築することを定義(22は比較的新しくてLTSなので採用)
FROM node:22.14.0-bullseye-slim
# Docker イメージをビルドする時の、コンテナ内作業ディレクトリを /app に設定
# このディレクトリを基準にして、この後のRUNやCOPYが実行される。
WORKDIR /app
# build用ARG の定義
ARG VITE_API_BASE_URL
ENV VITE_API_BASE_URL=${VITE_API_BASE_URL}

# npmパッケージのインストール開始
COPY package*.json ./
RUN npm install && chown -R 1000:1000 /app/node_modules
# vue.jsのビルドは-f development.yml run --rm frontendで開始

# # このDockerfileとdevelopment.ymlを使う場合、docker-compose -f development.yml up --buildでいい
# # 実行後は、http://localhost:8080でビルド後の結果を配信できる