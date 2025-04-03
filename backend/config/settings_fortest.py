# backend/config/settings_fortest.py
# テスト用の設定ファイル(settings.pyの内容も使ったうえで、上書き分や追加分が記述されている)

from .settings import *  # 全体の共通設定を引き継ぐ

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
