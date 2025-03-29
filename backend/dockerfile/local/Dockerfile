FROM python:3.12.9-slim

# # Rust & Cargoのインストール(drf-spectacularをインストールするのに)に必要なパッケージ
# RUN apt-get update && apt-get install -y \
#     curl \
#     build-essential \
#     libpq-dev \
#     && rm -rf /var/lib/apt/lists/*

# # Rust（+cargo）をインストール
# RUN curl https://sh.rustup.rs -sSf | sh -s -- -y
# ENV PATH="/root/.cargo/bin:$PATH"
WORKDIR /app
COPY ./backend/requirements/local.txt /app/requirements/local.txt
RUN pip install -r /app/requirements/local.txt

#---バックエンドで最初にやったこと----
# 1.docker-compose -f local.yml run --rm backend /bin/bashでログイン後、pip install でパッケージインストール → その後pip freeze > requirements/local.txtでtext化
# 入れたのはhttps://akiyoko.hatenablog.jp/entry/2022/12/23/075040を参考に
# djangorestframework django-allauth dj-rest-auth drf-spectacular django-cors-headers django-extensions django-filter django-storages
# 2. このDockerfileに、RUN pip install -r requirements/local.txtを追記
# 3. docker-compose -f local.yml run --rm backend django-admin startproject config . を実行して、プロジェクトを作成する
# 4. down --rmi all -v後に、build backendまたはup --build backend実行後、http://localhost:8000にアクセスして、最初のdjangoプロジェクトが画面がでることを確認する。
#--------
# ただし、3で生成されたファイル・ディレクトリは全部root所有になっていて、vscodeで編集できなくなっているので、
# ローカルでsudo chown -R $USER:$USER ./backendと、sudo chmod -R 777 ./backend を実行するか、
# コンテナ内で、chown -R 1000:1000 /appと、chmod -R 777 /appを実行しておきましょう。
# なお、migrationファイルの作成も、コンテナ内で実行 or docker-compose -f local.yml run --rm backend python3 makemigrationsで生成するはずですが、その後上記を実行しないと、生成したマイグレーションファイルを編集できなくなります。
#--------
# 上の注意部分を納得してもらってから、以降は、docker-compose up --build backendなどとして起動させてバックエンドの開発をすればok