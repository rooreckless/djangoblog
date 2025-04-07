# # playwright/e2etests/test_blog_list.py
import pytest
from playwright.sync_api import Page, Route, Request, expect
def test_pagetitle(page):
    # playwrightコンテナから、フロントエンドへアクセスする場合、localhost:5173ではなく、docker-composeのサービス名でのアクセスが必要
    page.goto("http://frontend:5173/blogs/")
    # page.content() # <- デバッグ用 playwrightが見ているpageのDOMを全部出力する
    # page.wait_for_selector("text=ブログ一覧")  # ← これで特定の要素が表示されるまで待つことができる(↓のexpectで待つことができるから不要だが)
    
    expect(page.get_by_test_id("section-title")).to_have_text("ブログ一覧")
    assert page.locator("text=ブログ一覧").is_visible() # ↑のexpectと.is_visible()以外はやっていることは一緒




@pytest.fixture
def mocked_blog_api_response():
    return {
        "results": [
            {"id": 1, "title": "モックタイトル", "contents_text": "これはモックされたブログです"},
            {"id": 2, "title": "モックタイトル2", "contents_text": "これはモックされたブログです2"},
            {"id": 3, "title": "モックタイトル3", "contents_text": "これはモックされたブログです3"},
            {"id": 4, "title": "モックタイトル4", "contents_text": "これはモックされたブログです4"}
        ],
        "current_page": 1,
        "num_of_items": 2,
        "num_of_pages": 1,
        "num_of_items_per_page": 10,
    }

def test_blog_list_with_mocked_api(page: Page, mocked_blog_api_response):
    def handle_route(route: Route, request: Request):
        if "/api/v1/blogs/" in request.url:
            route.fulfill(
                status=200,
                content_type="application/json",
                body=str(mocked_blog_api_response).replace("'", '"')  # JSONに変換
            )
        else:
            route.continue_()

    # モックを有効化
    page.route("**/api/v1/blogs/**", handle_route)

    page.goto("http://frontend:5173/blogs/")
    expect(page.get_by_test_id("section-title")).to_have_text("ブログ一覧")
    # expect(page.locator('[data-testid="blog-item"]')).to_have_count(4)
    expect(page.get_by_test_id("blog-item")).to_have_count(4)


#-----------

@pytest.fixture
def mocked_paginated_response2p():
    return {
        "page1": {
            "results": [
                {"id": 1, "title": "タイトル_1", "contents_text": "ページ1のブログ1"},
                {"id": 2, "title": "タイトル_2", "contents_text": "ページ1のブログ2"}
            ],
            "current_page": 1,
            "num_of_items": 4,
            "num_of_pages": 2,
            "num_of_items_per_page": 2,
        },
        "page2": {
            "results": [
                {"id": 3, "title": "タイトル_3", "contents_text": "ページ2のブログ1"},
                {"id": 4, "title": "タイトル_4", "contents_text": "ページ2のブログ2"}
            ],
            "current_page": 2,
            "num_of_items": 4,
            "num_of_pages": 2,
            "num_of_items_per_page": 2,
        }
    }

def test_pagination_next_page(page: Page, mocked_paginated_response2p):
    def handle_route(route: Route, request: Request):
        if "page=2" in request.url:
            route.fulfill(
                status=200,
                content_type="application/json",
                body=str(mocked_paginated_response2p["page2"]).replace("'", '"')
            )
        else:
            # page=1 or default
            route.fulfill(
                status=200,
                content_type="application/json",
                body=str(mocked_paginated_response2p["page1"]).replace("'", '"')
            )

    page.route("**/api/v1/blogs/**", handle_route)

    page.goto("http://frontend:5173/blogs/")
    expect(page.get_by_test_id("blog-item")).to_have_count(2)
    expect(page.locator("text=タイトル_1")).to_be_visible()
    expect(page.locator("text=タイトル_3")).not_to_be_visible()

    # 「次へ」ボタンをクリック
    # TODDO: datatestidを使う
    page.get_by_role("button", name="次へ").click()

    # 2ページ目のデータが表示されることを確認
    expect(page.get_by_test_id("blog-item")).to_have_count(2)
    expect(page.locator("text=タイトル_3")).to_be_visible()
    expect(page.locator("text=タイトル_1")).not_to_be_visible()

#-----------

@pytest.fixture
def blog_detail_response():
    return {
        "id": 1,
        "title": "モックタイトル",
        "contents_text": "モック本文",
        "created": "2025-04-04T12:00:00+09:00"
    }

@pytest.fixture
def blog_list_response():
    return {
        "results": [
            {"id": 1, "title": "モックタイトル", "contents_text": "モック本文"}
        ],
        "current_page": 1,
        "num_of_items": 1,
        "num_of_pages": 1,
        "num_of_items_per_page": 10,
    }

def test_blogs_title_click_navigates_to_detail(page: Page, blog_list_response, blog_detail_response):
    def handle_route(route: Route, request: Request):
        if "/api/v1/blogs/1/" in request.url:
            route.fulfill(
                status=200,
                content_type="application/json",
                body=str(blog_detail_response).replace("'", '"')
            )
        elif "/api/v1/blogs/" in request.url:
            route.fulfill(
                status=200,
                content_type="application/json",
                body=str(blog_list_response).replace("'", '"')
            )
        else:
            route.continue_()

    page.route("**/api/v1/blogs/**", handle_route)

    # 一覧ページを開く
    page.goto("http://frontend:5173/blogs/")
    expect(page.get_by_test_id("blog-title-link")).to_have_text("モックタイトル")

    # タイトルクリックで詳細へ遷移
    page.get_by_test_id("blog-title-link").click()

    # 詳細ページの要素が表示されているか確認
    expect(page.get_by_test_id("blog-title")).to_have_text("モックタイトル")
    expect(page.get_by_test_id("blog-contents-text")).to_have_text("モック本文")
    