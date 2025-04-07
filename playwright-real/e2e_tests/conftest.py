import os
import django
import pytest

# Django を初期化
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings_fortest")
django.setup()

from api.tests.factories.blogFactory import BlogFactory

@pytest.fixture
def create_sample_blogs():
    def _create(count=4):
        return BlogFactory.create_batch(count)
    return _create
