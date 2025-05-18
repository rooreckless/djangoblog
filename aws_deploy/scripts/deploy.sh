#!/bin/bash
set -e
set -x  # ← 追加：実行されるコマンドをすべて出力
echo "[deploy.sh] Starting application setup..."

sudo dnf install -y tree

echo "[deploy.sh] tree default"
pwd > /tmp/pwd1.log
ls -la > /tmp/ls1.log
tree . -a -L 3 > /tmp/tree1.log 2>&1

echo "[deploy.sh] tree top"
cd /
pwd > /tmp/pwd2.log
ls -la > /tmp/ls2.log
tree . -a -L 3 > /tmp/tree2.log 2>&1

echo "[deploy.sh] tree cded"
cd /home/ec2-user/app
pwd > /tmp/pwd3.log
ls -la > /tmp/ls3.log
tree . -a -L 3 > /tmp/tree3.log 2>&1


# Docker Compose 再起動（本番用のcomposeファイルがあればそちらに変更）
docker compose -f development.yml down || true
docker compose -f development.yml pull
docker compose -f development.yml up -d --build

echo "[deploy.sh] Docker containers are up."

# 必要に応じてマイグレーションや静的ファイル収集
docker compose -f development.yml exec -T backend python manage.py migrate --noinput
docker compose -f development.yml exec -T backend python manage.py collectstatic --noinput

echo "[deploy.sh] Deploy completed."
