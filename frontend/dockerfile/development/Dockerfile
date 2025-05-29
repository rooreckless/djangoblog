# マルチステージDockerfile(node.jsでビルド してから nginxでビルド結果を配信)
# slim系のnodeから構築することを定義(22は比較的新しくてLTSなので採用)
FROM node:22.14.0-bullseye-slim AS build-stage
# Docker イメージをビルドする時の、コンテナ内作業ディレクトリを /app に設定
# このディレクトリを基準にして、この後のRUNやCOPYが実行される。
WORKDIR /app
# build用ARG の定義
ARG VITE_API_HOST_ADDRESS
ENV VITE_API_HOST_ADDRESS=${VITE_API_HOST_ADDRESS}

# npmパッケージのインストール開始
COPY ./frontend/package*.json ./
RUN npm install && chown -R 1000:1000 /app/node_modules

COPY ./frontend .
RUN npm run build
# ----------------------------------------
# Production Stage（nginxでdistを配信）
FROM nginx:1.27.5-alpine3.21-slim AS deploy-stage
# frontendのビルド結果をnginxとして提供できるようにする
COPY --from=build-stage /app/dist /usr/share/nginx/html
# backendの静的ファイル(collectstaticを実行した成果物)も提供できるようにする
COPY  ./backend/static /static
# 任意のカスタムnginx.confがあるならコピー
COPY ./frontend/nginx/development/nginx.conf /etc/nginx/nginx.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]

# # このDockerfileとdevelopment.ymlを使う場合、docker-compose -f development.yml up --buildでいい
# # 実行後は、http://localhostでビルド後の結果を配信できる