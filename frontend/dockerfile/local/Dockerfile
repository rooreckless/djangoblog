# slim系のnodeから構築することを定義(22は比較的新しくてLTSなので採用)
FROM node:22.14.0-bullseye-slim
# Docker イメージをビルドする時の、コンテナ内作業ディレクトリを /app に設定
# このディレクトリを基準にして、この後のRUNやCOPYが実行される。
WORKDIR /app

#----------
#---このセクションの内容はdocke-compose build時に実行される内容で、その際にrootユーザーでは困る場合です。----
# # ビルド時にUIDとGIDを指定できるようにする（デフォルトは1000）
# ARG UID=1000
# ARG GID=1000



# # GIDが存在しない場合のみ、新しくグループappgroupを作成
# RUN getent group $GID || groupadd -g $GID appgroup

# # UIDが存在しない場合のみ、新しくユーザーappuserを作成
# RUN id -u $UID >/dev/null 2>&1 || useradd -m -u $UID -g $GID appuser


# # /app ディレクトリの所有者を appuser に変更（開発コードの所有者を合わせる）
# RUN chown -R $UID:$GID /app
# RUN chown -R $UID:$GID node_modules

# # `appuser` に切り替え（rootのまま起動しない）
# USER appuser

# ここに記述された内容が、appuserとして実行することになる。(ただし、npm installはできない←権限エラー)

#----------

COPY package*.json ./
RUN npm install

# デフォルトのコマンド。docker-composeでcommand指定するのでこの行は実行されないが一応指定。
CMD ["/bin/bash"]

# このdockerfileを使っている場合、
#----最初のプロジェクト作成手順は------
# 1
# viteプロジェクト作成 
# ↑docker-compose run --rm frontend npm create vite@latest . -- --template vue-ts
# ただし生成されたファイル・ディレクトリの所有者、所有グループがrootになっています。
# ローカルでsudo chown -R $USER:$USER ./frontendと、sudo chmod -R 777 ./frontend を実行するか、
# コンテナ内で、chown -R 1000:1000 /appと、chmod -R 777 /appを実行しておきましょう。
#----------
# 2
# tailwindcssインストールの参考先 https://tailwindcss.com/docs/installation/using-vite
# tailwindcssのインストール npm install tailwindcss @tailwindcss/vite
# ↑docker-compose run --rm frontend の引数に含めてやってもいいのは一緒
#---------
# 3 ここまで実行したら、package.jsonは作成されているはず

#---------
# 4 viteのHotRelaod設定と、tailwindcssの設定をしましょう
# 1でvite.config.jsが生成されているはずなので、HotReload設定しておきましょう。
# https://tailwindcss.com/docs/installation/using-viteに従い、vite.config.jsに追加と、cssファイルで@import "tailwindcss";を記述する
# 他にインストールしたいものがあるなら、docker-compose run --rm frontend npm install momentなどで可能(←momentを入れる例) = package.jsonが更新されるので

# 5 あとはdocker-compose up frontendを実行しましょう。

# 6 もしこの後で、docker-compose down --rmi all -vを実行したら、名前付きボリュームのnode_modulesが削除されます。
# それでも、docker-compose up --build frontendを実行したら、このDockerfileが実行される = npm installが行われるので、package.jsonからインストールされます。
# つまりソースコードが残っているなら、問題なく起動できるはずです。

#----
# もし必要なライブラリを追加したくなったら、frontendコンテナが動いている状態ならば、
# docker-compose -f local.yml exec frontend /bin/bashでログイン後に、npm install しましょう。
# たとえばhttps://router.vuejs.org/installation.htmlを参考に、 npm install vue-router とします。
# 他にもhttps://pinia.vuejs.org/getting-started.htmlからpiniaを、https://headlessui.com/v1/vue からheadless uiをいれたりもしています。
# さらにvee-validateはhttps://vee-validate.logaretm.com/v4/guide/overview/ から、yupはhttps://www.npmjs.com/package/yup からです。
# https://reffect.co.jp/vue/veevaliate4