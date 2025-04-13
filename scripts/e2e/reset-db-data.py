# scripts/reset-db-data.py
import os
import psycopg # PostgreSQL に接続するためのライブラリ（psycopg v3）
from psycopg import sql
# 環境変数から DB 接続情報を取得し、接続を作成
conn = psycopg.connect(
    host=os.environ["POSTGRES_HOST"],         # DBホスト（通常は"postgres"など）
    dbname=os.environ["POSTGRES_DB"],         # DB名（例: "djangoblog"）
    user=os.environ["POSTGRES_USER"],         # DBユーザー名
    password=os.environ["POSTGRES_PASSWORD"], # DBパスワード
    port=os.environ["POSTGRES_PORT"],         # ポート番号（通常は5432）
)

#-------------------------------------
# # 「リセット方法 その1」 指定したテーブルだけリセットする(IDもまきもどす)
# # トランザクション管理ブロックを開始（with を使うと自動的に commit / rollback）
# with conn:
#     # カーソルを開いてSQLを実行する（クエリの送信）
#     with conn.cursor() as cur:
#         # Blogモデルに対応するテーブル "api_blog" を初期化
#         cur.execute("TRUNCATE TABLE api_blog RESTART IDENTITY CASCADE;")
#         # - TRUNCATE TABLE: テーブルのすべてのデータを削除
#         # - RESTART IDENTITY: ID（主キー）を1から振り直す
#         # - CASCADE: 外部キー制約がある関連テーブルも一緒に削除
# print("✅ DB 全テーブルの初期化が完了しました")
# # もし複数のテーブルをリセットしたい場合は以下のwithのなかを以下にする
# # cur.execute("TRUNCATE TABLE api_comment, api_blog RESTART IDENTITY CASCADE;")
#-------------------------------------

# --「リセット方法 その2」 リセット対象を絞って全テーブル指定リセット(ID巻き戻しも含む)の部分--
# excluded_tables = 削除対象から除外したいテーブルの名前一覧
excluded_tables = {
    "django_migrations", # マイグレーションの履歴（手動でレコードを消すわけにいかないテーブル）
    "django_content_type", # モデルとパーミッションを関連付けている（削除非推奨）
    "auth_permission", # Djangoの組み込みパーミッション（消しても再生成されるが注意が必要）
}

# トランザクション管理ブロックを開始（with を使うと自動的に commit / rollback）
with conn:
    # カーソルを開いてSQLを実行する（クエリの送信）
    with conn.cursor() as cur:
        # クエリを組み立てる
        # 内容は、「PostgreSQL のメタテーブル pg_tables」から、
        # 「スキーマが 'public' に属している」かつ 「excluded_tables に含まれていないテーブル名」をすべて取得。
        # この段階ではクエリを準備しているだけ
        query = sql.SQL("""
            SELECT tablename FROM pg_tables
            WHERE schemaname = 'public'
              AND tablename NOT IN ({})
        """).format(sql.SQL(', ').join(sql.Placeholder() * len(excluded_tables)))
        # クエリを実行
        # 実行結果結果は tables = cur.fetchall() にリストで格納され、たとえば [(api_blog,), (auth_user,), ...] のようになります。
        cur.execute(query, tuple(excluded_tables))
        tables = cur.fetchall()
        # 削除対象のテーブルはtablesに入っているので要素ごとに、レコード全削除SQLを実行する
        for (table,) in tables:
            cur.execute(
                sql.SQL('TRUNCATE TABLE {} RESTART IDENTITY CASCADE;')
                .format(sql.Identifier(table))
            )
            # - TRUNCATE TABLE: テーブルのすべてのデータを削除
            # - RESTART IDENTITY: ID（主キー）を1から振り直す
            # - CASCADE: 外部キー制約がある関連テーブルも一緒に削除
print("✅ アプリとして定義したテーブルのみ初期化しました")
#-------------------------------------

# 実行するコマンド
# docker compose -f e2e.yml run --rm backend python3 scripts/reset-db-data.py