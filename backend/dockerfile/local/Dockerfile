FROM python:3.12.9-slim
WORKDIR /app
COPY ./backend/requirements/local.txt /app/requirements/local.txt
RUN pip install --upgrade pip && pip install -r /app/requirements/local.txt

#--0 バックエンドで最初にやったこと--
# 1.docker-compose -f local.yml run --rm backend /bin/bashでログイン後、pip install でパッケージインストール → その後pip freeze > requirements/local.txtでtext化
# 入れたのはhttps://akiyoko.hatenablog.jp/entry/2022/12/23/075040を参考に
# djangorestframework django-allauth dj-rest-auth drf-spectacular django-cors-headers django-extensions django-filter django-storages psycopg2
# 2. このDockerfileに、RUN pip install -r requirements/local.txtを追記
# 3. docker-compose -f local.yml run --rm backend django-admin startproject config . を実行して、プロジェクトを作成する
# 4. down --rmi all -v後に、build backendまたはup --build backend実行後、http://localhost:8000にアクセスして、最初のdjangoプロジェクトが画面がでることを確認する。
#--------
# ===OLD情報====
# ただし、3で生成されたファイル・ディレクトリは全部root所有になっていて、vscodeで編集できなくなっているので、
# ローカルでsudo chown -R $USER:$USER ./backendと、sudo chmod -R 777 ./backend を実行するか、
# コンテナ内で、chown -R 1000:1000 /appと、chmod -R 777 /appを実行しておきましょう。
# なお、migrationファイルの作成も、コンテナ内で実行 or docker-compose -f local.yml run --rm backend python3 makemigrationsで生成するはずですが、その後上記を実行しないと、生成したマイグレーションファイルを編集できなくなります。
#--------
# 上の注意部分を納得してもらってから、以降は、docker-compose up --build backendなどとして起動させてバックエンドの開発をすればok
# 【OLD情報に対する追記】user: "${UID:-1000}:${GID:-1000}"をdocker-compose.ymlに書き込んでいるので、docker-composeコマンドを使う時はuid=1000でログインする。
# その状態で生成されるファイルは1000:1000の所有者・所有グループとなる。なので問題ない。
# =============

#--1 フロントからバックに通信できるようになるまで、バックエンド側--
# 1 アプリの作成(→ではapiというディレクトリができる)  docker-compose -f local.yml run --rm backend python manage.py startapp api
# ↑コマンドで作成しているので、apiディレクトリ自体の権限の変更は必要になる。
# 2 modelsを作成してモデル(blogs.py)を作成 参考は https://qiita.com/okoppe8/items/a1149b2be54441951de1#%E6%96%87%E5%AD%97%E5%88%97textfield
# 3 シリアライザ(rest_framewor.serializers.ModelSerializerを継承したクラス)、ビュー（検証段階ならrest_framewor.viewsets.ReadOnlyModelViewSetを継承したクラス）を作成し、urls.pyにビューのpathをrouter.registerする
# 4 psycopg[binary]をpip install される状態にしないとエラーになる。https://github.com/psycopg/psycopg
# 5 settings.pyのDATABASESの設定をdocker-composeからの環境変数をつかうようにすること。またINSTALLED_APPSにもapiを登録する必要がでる。
# 5 docker compose -f local.yml run --rm backend python manage.py makemigrations でマイグレーションファイルを作成 (権限変更が必要なのは一緒)
# 6 docker compose -f local.yml run --rm backend python manage.py migrate
# 7 docker compose -f local.yml run --rm backend python manage.py createsuperuser --noinput
# 8 あとはlistとretrieveなルーティングを実現する