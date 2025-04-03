#!/bin/bash
# バックエンドのマイグレーション + スーパーユーザー作成 + サンプルデータ作成をするスクリプト
# まだこのスクリプトのうちcreate_sampledateだけは未実装です。

# docker compose -f local.yml run --rm backend python manage.py migrate  && docker compose -f local.yml run --rm backend python manage.py createsuperuser --no-input && docker compose -f local.yml run --rm django python manage.py create_sample_data
docker compose -f local.yml run --rm backend python manage.py migrate  && docker compose -f local.yml run --rm backend python manage.py createsuperuser --no-input

if [ $? -eq 0 ]; then
    echo "正常に終了しました。"
else
    echo "スクリプトが失敗しました"
fi