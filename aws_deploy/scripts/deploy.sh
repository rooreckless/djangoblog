#!/bin/bash
set -e

cd /home/ec2-user/app

echo "[deploy.sh] Starting application setup..."

# Docker Compose 再起動（本番用のcomposeファイルがあればそちらに変更）
docker compose -f development.yml down || true
docker compose -f development.yml pull
docker compose -f development.yml up -d --build

echo "[deploy.sh] Docker containers are up."

# 必要に応じてマイグレーションや静的ファイル収集
docker compose -f development.yml exec -T backend python manage.py migrate --noinput
docker compose -f development.yml exec -T backend python manage.py collectstatic --noinput

echo "[deploy.sh] Deploy completed."
