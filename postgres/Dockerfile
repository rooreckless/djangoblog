FROM postgres:15

# healthcheck用の スクリプトをコピー
COPY ./check-db.sh /usr/local/bin/check-db.sh

# そのスクリプトに実行権限をつける
RUN chmod +x /usr/local/bin/check-db.sh
