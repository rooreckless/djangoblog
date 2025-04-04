#!/bin/bash
# バックエンドのマイグレーション + スーパーユーザー作成 + サンプルデータ作成をするスクリプト
# 実行する時は scriptsディレクトリがあるところ= djangoblogディレクトリで、sh setup-script.shで実行してください。
docker compose -f local.yml run --rm backend python manage.py migrate  && docker compose -f local.yml run --rm backend python manage.py createsuperuser --no-input && docker compose -f local.yml run --rm backend python manage.py create_sample_data

if [ $? -eq 0 ]; then
    echo "正常に終了しました。"
else
    echo "スクリプトが失敗しました"
fi