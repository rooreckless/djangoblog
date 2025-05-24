#!/bin/bash
# このスクリプト(codedeployのappspec.ymlでは、set -xやset -eは使えないことを確認)
# スクリプト実行時の様子は、/opt/codedeploy-agent/deployment-root/<ランダムな数字>54c7fbda-2fb5-462d-98df-94ee1a0b8ed1/d-5GOOB6ZKC/logs
echo "[deploy.sh] 実行開始"
echo "[deploy.sh] カレントディレクトリの状況確認"
pwd > /tmp/pwd1.log         # <- この出力は /
ls -la > /tmp/ls1.log       # この中に、development.ymlが存在しない。あるとしたら、/home/ec2-user/appの中
echo $(pwd)
echo $(ls -la)
# cd /home/ec2-user/app


# Docker Compose 再起動（本番用のcomposeファイルがあればそちらに変更）
echo "[deploy.sh] コンテナを停止"
docker compose -f development.yml down || true
echo "[deploy.sh] コンテナビルドしなおしと、起動"
docker compose -f development.yml build
docker compose -f development.yml up -d
echo "[deploy.sh] コンテナ起動完了"

# 必要に応じてマイグレーションや静的ファイル収集
echo "[deploy.sh] バックエンド(gunicorn)コンテナ マイグレーション開始"
docker compose -f development.yml run --rm backend_gunicorn python manage.py migrate
echo "[deploy.sh] バックエンド(gunicorn)コンテナ collectstatic 開始"
docker compose -f development.yml run --rm backend_gunicorn python manage.py collectstatic --noinput

# スーパーユーザー作成とサンプルデータ作成はEC2にログインして実施してください。


echo "[deploy.sh] Deploy 完了."