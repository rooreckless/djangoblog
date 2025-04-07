# # playwright/e2etests/conftest.py

# import os
# import django
# import pytest

# # Django を初期化する（DJANGO_SETTINGS_MODULE を設定）
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings_fortest')
# django.setup()

# from api.models.blogs import Blog  # ← Django モデルの import

# @pytest.fixture
# def create_sample_blogs():
#     def make(count=5):
#         for i in range(count):
#             Blog.objects.create(title=f"テストタイトル_{i}", contents_text=f"テスト内容_{i}")
#     return make