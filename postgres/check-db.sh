#!/bin/bash
# DBのヘルスチェックに使うスクリプト
# 環境変数 POSTGRES_USER と POSTGRES_DB を使って readiness check
pg_isready -U "$POSTGRES_USER" -d "$POSTGRES_DB"