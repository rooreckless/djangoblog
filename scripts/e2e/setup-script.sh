#!/bin/bash
#---------------
# e2eテスト用の前準備スクリプトの1つめ
# docker compose -f e2e.yml up --build
# で起動後は、
# sh scripts/e2e/setup-script.sh
# で実行してください。
# バックエンドのマイグレーション + スーパーユーザー作成 をします。
# (実行する時は scriptsディレクトリがあるところ= djangoblogディレクトリで)
#---------------
echo "--1 migrate--e2e_tests--" && \
docker compose -f e2e.yml run --rm backend python manage.py migrate  && \
echo "--2 createsuperuser--e2e_tests--" && \
docker compose -f e2e.yml run --rm backend python manage.py createsuperuser --no-input
# echo "--3 create_e2etest_data" && \
# docker compose -f e2e.yml run --rm backend python manage.py create_e2etest_data && \
# echo "--4 start--e2e_tests--" && \
# docker compose -f e2e.yml run --rm playwright-real pytest e2e_tests  || true && \
# echo "--5 resetdb--e2e_tests--" && \
# docker compose -f e2e.yml run --rm backend python3 scripts/reset-db-data.py
if [ $? -eq 0 ]; then
    echo "正常に終了しました。"
else
    echo "スクリプトが失敗しました"
fi