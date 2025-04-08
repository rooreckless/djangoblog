# backend/config/settings_fortest.py
# テスト用の設定ファイル(settings.pyの内容も使ったうえで、上書き分や追加分が記述されている)

from .settings import *  # 全体の共通設定を引き継ぐ
import os

SECRET_KEY = "test-only-secret-key"

TEST_RUNNER = "django.test.runner.DiscoverRunner"

# # パスワードハッシュを高速なMD5に（テストなので強度不要）
# PASSWORD_HASHERS = [
#     "django.contrib.auth.hashers.MD5PasswordHasher",
# ]

# # メールを実際に送信せず、メモリ内に保存（テスト用）
# EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"

# テンプレートデバッグ有効化（エラー表示が分かりやすく）
TEMPLATES[0]["OPTIONS"]["debug"] = True  # type: ignore

# テスト用DB名を明示的に設定
DATABASES["default"]["TEST"] = {
    # NAMEが開発用のdjangoblogと同じだと、テスト実行後に全レコードがきえてします。なのでe2eテスト専用DB名を与える必要があった。
    "NAME": "test_djangoblog",
    "MIRROR": None,
    "DEPENDENCIES": [],
    "SERIALIZE": False,
    "CREATE_DB": False,  # ← これが重要！
}

# まだこのファイルを使う場合はCORSとして通すORIGINは全部
CORS_ALLOWED_ORIGINS = ["http://frontend:5173"] # バックエンドへのテストができない
# CORS_ALLOW_ALL_ORIGINS = True
# バックエンドとして受け付けるホスト。これがないと
ALLOWED_HOSTS = [
    # "localhost",
    # "127.0.0.1",
    "backend",  # ← docker-compose 内でのホスト名 これがないとエラーになる
    # "frontend", # ← なくてもテストは可能
]

# このsettingsで使うDB名を確認するため使う
# print("[settings_fortest] POSTGRES_DB =", os.environ.get("POSTGRES_DB"))
# print("[settings_fortest] NAME =", DATABASES["default"]["NAME"])
