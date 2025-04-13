#----------
# e2eテスト時は、djangoblogDBをそのまま使う(pytest-djangoによる「test_~なDBの自動作成」にたよらない)
# なので「このファイルでフィクスチャを使ってテスト前データ準備する」としても「apiを叩いてデータを準備する」などのやり方になる。
# playwright-realコンテナではbackendのソースコードをマウントしないので、djangoのORMが使えないからです
#----------
# import os
# import django
# import pytest

# @pytest.fixture
# def create_sample_blogs():
# ↓の内容そのものは使えないけど、フィクスチャとして定義の仕方としてはこの通り
#     def _create(count=1):
#         blogs = BlogFactory.create_batch(count)
#         # このフィクスチャをお使った場合のファクトリによって作成されたブログの件数を書くにする
#         # print("Blog.objects.all().count()=", Blog.objects.all().count())  # デバッグ用
#         return blogs
#     return _create