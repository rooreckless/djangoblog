# playwright/e2etests/test_blog_list.py
import pytest
from playwright.sync_api import expect
def test_blog_list_shows_blogs(page):
    # playwrightコンテナから、フロントエンドへアクセスする場合、localhost:5173ではなく、docker-composeのサービス名でのアクセスが必要
    page.goto("http://frontend:5173/blogs/")
    # page.content() # <- デバッグ用 playwrightが見ているpageのDOMを全部出力する
    # page.wait_for_selector("text=ブログ一覧")  # ← これで特定の要素が表示されるまで待つことができる(↓のexpectで待つことができるから不要だが)
    
    expect(page.get_by_test_id("section_title")).to_have_text("ブログ一覧")
    # assert page.locator("text=ブログ一覧").is_visible() # ↑のexpectとやっていることは一緒
    