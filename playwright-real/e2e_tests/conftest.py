import os
import django
import pytest

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings_fortest")
os.environ.setdefault("DJANGO_ALLOW_ASYNC_UNSAFE", "true")

django.setup()

from api.tests.factories.blogFactory import BlogFactory
from api.models.blogs import Blog

@pytest.fixture
def create_sample_blogs():
    def _create(count=1):
        blogs = BlogFactory.create_batch(count)
        # このフィクスチャをお使った場合のファクトリによって作成されたブログの件数を書くにする
        # print("Blog.objects.all().count()=", Blog.objects.all().count())  # デバッグ用
        return blogs
    return _create