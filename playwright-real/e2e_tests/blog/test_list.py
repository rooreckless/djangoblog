# e2eテスト用
import pytest
from playwright.sync_api import Page, expect
from api.models.blogs import Blog
@pytest.mark.django_db(transaction=True)
def test_blog_list_with_real_db(page: Page, create_sample_blogs):
    # 実データを作成
    create_sample_blogs(count=4)
    print("Blog.objects.all().count()=",Blog.objects.all().count())
    # フロントにアクセス
    page.goto("http://frontend:5173/blogs/")

    # 検証
    expect(page.get_by_test_id("section-title")).to_have_text("ブログ一覧")
    expect(page.get_by_test_id("blog-item")).to_have_count(4)
