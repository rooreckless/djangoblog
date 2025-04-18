import pytest
from playwright.sync_api import Page, Route, Request, expect

@pytest.mark.parametrize("route_status", [201])
def test_create_blog_success(page: Page, route_status):
    # モック: POST /api/v1/blogs/ に対して成功レスポンスを返す
    def handle_blog_create(route: Route, request: Request):
        assert request.method == "POST"
        payload = request.post_data_json
        assert "title" in payload
        assert "contents_text" in payload
        route.fulfill(
            status=route_status,
            content_type="application/json",
            body='{"id": 1, "title": "モックタイトル", "contents_text": "モック本文"}'
        )
    
    page.route("**/api/v1/blogs/", handle_blog_create)

    # フロントエンドの作成画面へ遷移
    page.goto("http://frontend:5173/blogs/create")

    # 入力フォームにデータを入力
    page.get_by_test_id("blogcreate-input-title").fill("モックタイトル")
    page.get_by_test_id("blogcreate-textarea-contents-text").fill("モック本文")

    # 送信ボタンをクリック
    page.get_by_test_id("blogcreate-back-btn").click()

    # 成功した場合の挙動を検証（例：トップページに戻る）
    expect(page).to_have_url("http://frontend:5173/blogs")
