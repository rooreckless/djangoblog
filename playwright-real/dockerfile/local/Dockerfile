# FROM mcr.microsoft.com/playwright/python:v1.44.0-jammy
FROM mcr.microsoft.com/playwright/python:v1.51.0-noble
WORKDIR /app

# 必要なパッケージのインストール
COPY ./playwright-real/dockerfile/local/requirements.txt /app/requirements-e2e-real.txt
COPY ./backend/requirements/local.txt /app/requirements-django.txt
RUN pip install --upgrade pip && pip install -r requirements-e2e-real.txt && pip install -r requirements-django.txt

# Playwrightのブラウザをインストール（必要に応じて）
RUN playwright install

# ----
# 【このplaywrightコンテナを使ったテストを実施する方法】
# 1. フロントエンドコンテナが動いていること : docker compose -f local.yml up または docker compose -f local.yml up frontend
# 2. テストの実施 : docker compose -f local.yml --profile e2e-mock run --rm playwright pytest mocked_tests
# docker compose -f local.yml --profile e2e-mock run --rm playwright pytest e2e_tests
# ----
# 【2の補足】
# ディレクトリやテストケースファイルを絞りったり、テストケース・メソッドをしぼりたいなら、
# docker compose -f local.yml --profile e2e-mock run --rm playwright pytest e2e_tests/test_dir/test_file.py::test_case_method
# docker compose -f local.yml run --rm playwright pytest e2e_tests/test_dir/test_file.py::test_case_method
# print文の出力もしたいなら pytestコマンドに -sも追加する

# ----
# 【テスト時にビデオを出力したりする方法】
# テスト時のビデオの出力とトレースデータも出力するコマンド
# docker compose -f local.yml --profile e2e-mock run --rm playwright pytest e2e_tests/test_sample.py --video=on --tracing=on
# 出力されたトレースデータを見るコマンド(プロジェクトルートディレクトリで実行しているとする)(ローカルPC自体にnode.jsのインストールを必要とする)
# npx playwright show-trace <トレース結果のzipファイルまでの相対パス>