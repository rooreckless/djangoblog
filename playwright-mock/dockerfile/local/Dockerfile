# FROM mcr.microsoft.com/playwright/python:v1.44.0-jammy
FROM mcr.microsoft.com/playwright/python:v1.51.0-noble
WORKDIR /app

# 必要なパッケージのインストール
COPY ./playwright-mock/dockerfile/local/requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

# Playwrightのブラウザをインストール（必要に応じて）
RUN playwright install

# ----
# 【このplaywrightコンテナを使ったテストを実施する方法】
# 1. フロントエンドコンテナが動いていること : docker compose -f local.yml up または docker compose -f local.yml up frontend
# 2. テストの実施 : docker compose -f local.yml --profile e2e-mock run --rm playwright-mock pytest mocked_tests
# docker compose -f local.yml --profile e2e-mock run --rm playwright-mock pytest
# ----
# 【2の補足】
# ディレクトリやテストケースファイルを絞りったり、テストケース・メソッドをしぼりたいなら、
# docker compose -f local.yml --profile e2e-mock run --rm playwright-mock pytest mocked_tests/blog/test_list.py::test_pagetitle
# print文の出力もしたいなら pytestコマンド部分に -sも追加する

# ----
# 【テスト時にビデオを出力したりする方法】
# テスト時のビデオの出力とトレースデータも出力するコマンド
# docker compose -f local.yml --profile e2e-mock run --rm playwright-mock pytest mocked_tests/blog/test_list.py --video=on --tracing=on
# 出力されたトレースデータを見るコマンド(プロジェクトルートディレクトリで実行しているとする)(ローカルPC自体にnode.jsのインストールを必要とする)
# npx playwright show-trace <トレース結果のzipファイルまでの相対パス>