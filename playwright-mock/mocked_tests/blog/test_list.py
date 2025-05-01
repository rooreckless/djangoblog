# # playwright/e2etests/test_blog_list.py
import pytest, json, os
from playwright.sync_api import Page, Route, Request, expect
def test_pagetitle(page):
    # playwrightコンテナから、フロントエンドへアクセスする場合、localhost:5173ではなく、docker-composeのサービス名でのアクセスが必要
    base_url = os.environ.get("BASE_URL")
    # page.goto("http://frontend:5173/blogs/")
    # page.goto('http://front_nginx/blogs/')
    page.goto(f"{base_url}/blogs")
    # page.content() # <- デバッグ用 playwrightが見ているpageのDOMを全部出力する
    # page.wait_for_selector("text=ブログ一覧")  # ← これで特定の要素が表示されるまで待つことができる(↓のexpectで待つことができるから不要だが)
    
    expect(page.get_by_test_id("bloglist-section-title")).to_have_text("ブログ一覧")
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
    base_url = os.environ.get("BASE_URL")

    
    # page.goto("http://frontend:5173/blogs/")
    # page.goto('http://front_nginx/blogs/')
    page.goto(f"{base_url}/blogs")
    expect(page.get_by_test_id("bloglist-section-title")).to_have_text("ブログ一覧")
    # expect(page.locator('[data-testid="bloglist-blog-item"]')).to_have_count(4)
    expect(page.get_by_test_id("bloglist-blog-item")).to_have_count(4)


#-----------

@pytest.fixture
def mocked_paginated_response2p():
    return {
        "page1": {
            "results": [
                {"id": 1, "title": "タイトル_1", "contents_text": "ページ1のブログ1"},
                {"id": 2, "title": "タイトル_2", "contents_text": "ページ1のブログ2"},
                {"id": 3, "title": "タイトル_3", "contents_text": "ページ1のブログ3"},
                {"id": 4, "title": "タイトル_4", "contents_text": "ページ1のブログ4"},
                {"id": 5, "title": "タイトル_5", "contents_text": "ページ1のブログ5"},
                {"id": 6, "title": "タイトル_6", "contents_text": "ページ1のブログ6"},
                {"id": 7, "title": "タイトル_7", "contents_text": "ページ1のブログ7"},
                {"id": 8, "title": "タイトル_8", "contents_text": "ページ1のブログ8"},
                {"id": 9, "title": "タイトル_9", "contents_text": "ページ1のブログ9"},
                {"id": 10, "title": "タイトル_10", "contents_text": "ページ1のブログ10"},
            ],
            "current_page": 1,
            "num_of_items": 20,
            "num_of_pages": 2,
            "num_of_items_per_page": 10,
        },
        "page2": {
            "results": [
                
                {"id": 11, "title": "タイトル_11", "contents_text": "ページ2のブログ1"},
                {"id": 12, "title": "タイトル_12", "contents_text": "ページ2のブログ2"},
                {"id": 13, "title": "タイトル_13", "contents_text": "ページ2のブログ3"},
                {"id": 14, "title": "タイトル_14", "contents_text": "ページ2のブログ4"},
                {"id": 15, "title": "タイトル_15", "contents_text": "ページ2のブログ5"},
                {"id": 16, "title": "タイトル_16", "contents_text": "ページ2のブログ6"},
                {"id": 17, "title": "タイトル_17", "contents_text": "ページ2のブログ7"},
                {"id": 18, "title": "タイトル_18", "contents_text": "ページ2のブログ8"},
                {"id": 19, "title": "タイトル_19", "contents_text": "ページ2のブログ9"},
                {"id": 20, "title": "タイトル_20", "contents_text": "ページ2のブログ10"},
            ],
            "current_page": 2,
            "num_of_items": 20,
            "num_of_pages": 2,
            "num_of_items_per_page": 10,
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

    base_url = os.environ.get("BASE_URL")
    # page.goto("http://frontend:5173/blogs/")
    # page.goto('http://front_nginx/blogs/')
    page.goto(f"{base_url}/blogs")
    expect(page.get_by_test_id("bloglist-blog-item")).to_have_count(10)
    expect(page.get_by_test_id("bloglist-blog-title-1")).to_be_visible()
    expect(page.get_by_test_id("bloglist-blog-title-13")).not_to_be_visible()
    
    # 「次へ」ボタンをクリック
    # page.get_by_role("button", name="次へ").click()
    page.get_by_test_id("bloglist-nextpage-btn").click()
    

    # 2ページ目のデータが表示されることを確認
    expect(page.get_by_test_id("bloglist-blog-item")).to_have_count(10)
    expect(page.get_by_test_id("bloglist-blog-title-13")).to_be_visible()
    expect(page.get_by_test_id("bloglist-blog-title-1")).not_to_be_visible()
    
#-----------

@pytest.fixture
def blog_detail_response():
    return {
        "id": 1,
        "title": "モックタイトル1",
        "contents_text": "モック本文1",
        "created": "2025-04-04T12:00:00+09:00"
    }

@pytest.fixture
def blog_list_response():
    return {
        "results": [
            {"id": 1, "title": "モックタイトル1", "contents_text": "モック本文1"},
            {"id": 2, "title": "モックタイトル2", "contents_text": "モック本文2"},
            {"id": 3, "title": "モックタイトル3", "contents_text": "モック本文3"},
            {"id": 4, "title": "モックタイトル4", "contents_text": "モック本文4"},
            {"id": 5, "title": "モックタイトル5", "contents_text": "モック本文5"},
            {"id": 6, "title": "モックタイトル6", "contents_text": "モック本文6"},
            {"id": 7, "title": "モックタイトル7", "contents_text": "モック本文7"},
            {"id": 8, "title": "モックタイトル8", "contents_text": "モック本文8"},
            {"id": 9, "title": "モックタイトル9", "contents_text": "モック本文9"},
            {"id": 10, "title": "モックタイトル10", "contents_text": "モック本文10"}
        ],
        "current_page": 1,
        "num_of_items": 10,
        "num_of_pages": 1,
        "num_of_items_per_page": 10,
    }

def test_blogs_title_click_navigates_to_detail(page: Page, blog_list_response, blog_detail_response):
    
    def handle_route_bloglist(route: Route, request: Request):
        if "/api/v1/blogs/" in request.url:
            route.fulfill(
                status=200,
                content_type="application/json",
                body=str(blog_list_response).replace("'", '"')  # JSONに変換
            )
        else:
            route.continue_()
    
    def handle_route_blogretrieve1(route: Route, request: Request):
        if "/api/v1/blogs/1" in request.url:
            route.fulfill(
                status=200,
                content_type="application/json",
                body=str(blog_detail_response).replace("'", '"')  # JSONに変換
            )
        else:
            route.continue_()
    

    page.route("**/api/v1/blogs/**", handle_route_bloglist)
    page.route("**/api/v1/blogs/1/**", handle_route_blogretrieve1)
    # 一覧ページを開く
    base_url = os.environ.get("BASE_URL")
    # page.goto("http://frontend:5173/blogs/")
    # page.goto('http://front_nginx/blogs/')
    page.goto(f"{base_url}/blogs")

    expect(page.get_by_test_id("bloglist-blog-title-1")).to_have_text("モックタイトル1")

    # タイトルクリックで詳細へ遷移
    page.get_by_test_id("bloglist-blog-title-link-1").click()

    # 詳細ページの要素が表示されているか確認
    expect(page.get_by_test_id("blogretrive-blog-title")).to_have_text("モックタイトル1")
    expect(page.get_by_test_id("blogretrive-blog-contents-text")).to_have_text("モック本文1")
    