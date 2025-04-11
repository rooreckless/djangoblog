#!/bin/bash
#---------------
# e2eテスト用の前準備スクリプトの2つめ
# docker compose -f e2e.yml up --build
# で起動後に、
# sh scripts/e2e/setup-script.sh
# でバックエンドのマイグレーション + スーパーユーザー作成 をした後に、
# sh scripts/e2e/e2etest-script.sh
# (実行する時は scriptsディレクトリがあるところ= djangoblogディレクトリで)
#---------------
# 【このスクリプトでやっていること】
# e2eテストで使うデータを作成して、テストを実施、実施後は作成したデータを削除する。
# テスト結果にfailやエラーがあれば、e2e_tests/test-resultsにトレースデータ保存される(トレースデータを見る場合は、npx palywright show-trace そのトレースデータへの相対パス で確認可能)
echo "--1 create_e2etest_data" && \
docker compose -f e2e.yml run --rm backend python manage.py create_e2etest_data && \
echo "--2 start--e2e_tests--" && \
docker compose -f e2e.yml run --rm playwright-real pytest e2e_tests \
  --video=retain-on-failure \
  --tracing=retain-on-failure \
  --output=e2e_tests/test-results  || true && \
echo "--3 resetdb--e2e_tests--" && \
docker compose -f e2e.yml run --rm backend python3 scripts/reset-db-data.py
if [ $? -eq 0 ]; then
    echo "正常に終了しました。"
else
    echo "スクリプトが失敗しました"
fi