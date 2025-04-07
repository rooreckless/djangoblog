# e2eテスト用
import pytest
from playwright.sync_api import Page, expect
from api.models.blogs import Blog
from django.db import connection

@pytest.mark.django_db(transaction=True)
def test_blog_list_with_real_db(page: Page, create_sample_blogs):
    create_sample_blogs(count=4)
    # フィクスチャによって作成されたレコード数の確認
    print("Blog.objects.all().count()=",Blog.objects.all().count())
    # このテストケース中に接続しているDB名の確認
    print("接続中のデータベース名:", connection.settings_dict["NAME"])
    with connection.cursor() as cursor:
        cursor.execute("SELECT current_database();")
        db_name = cursor.fetchone()[0]
        # SQLでもDB名を確認
        print("current_database() =", db_name)
    # ブログ一覧ページへ移動
    # ブラウザから表示（ここでは JS 側で localhost:8000 を参照している想定）
    page.goto("http://frontend:5173/blogs/")
    # ブログ一覧で描画されるhtml全体を確認したい場合
    # print(page.content())

    # UI検証
    # ブログ一覧を表示しているかを確認する
    # print("---",page.get_by_test_id("section-title").inner_text())
    expect(page.get_by_test_id("section-title")).to_have_text("ブログ一覧")
    
    # DBからのブログレコードを一覧表示できているか確認する
    expect(page.get_by_test_id("blog-item")).to_have_count(4)
    # print("-=-",page.get_by_test_id("blog-item"))
    # 一覧表示しているブログの内容を表示している(念の為)
    # items = page.get_by_test_id("blog-item").all()
    # for i, item in enumerate(items):
    #     print(f"[item {i}] {item.inner_text()}")