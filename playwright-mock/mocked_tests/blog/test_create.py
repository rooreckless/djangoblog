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

    # 送信ボタンをクリック ← ブログが作成されたはず
    page.get_by_test_id("blogcreate-back-btn").click()

    # 成功した場合の挙動を検証 = ブログ一覧ページに戻っているはず
    expect(page).to_have_url("http://frontend:5173/blogs")


def test_create_blog_with_empty_fields(page: Page):
    page.goto("http://frontend:5173/blogs/create")

    # 何も入力せずに送信ボタンをクリック ← ブログ作成はされないはず
    page.get_by_test_id("blogcreate-submit-btn").click()

    # バリデーションエラーになるはずなので、メッセージがでているかの検証
    expect(page.get_by_test_id("blogcreate-input-title-error")).to_be_visible()
    expect(page.get_by_test_id("blogcreate-textarea-contents-text-error")).to_be_visible()
    # エラーメッセージの内容を検証
    expect(page.get_by_test_id("blogcreate-input-title-error")).to_have_text("タイトルは必須です")
    expect(page.get_by_test_id("blogcreate-textarea-contents-text-error")).to_have_text("本文は必須です")



def test_create_blog_with_title_too_long(page: Page):
    page.goto("http://frontend:5173/blogs/create")

    # 201文字のタイトルを入力
    long_title = "あ" * 201
    page.get_by_test_id("blogcreate-input-title").fill(long_title)

    # 本文は正常値を入力
    page.get_by_test_id("blogcreate-textarea-contents-text").fill("本文の内容")

    # 送信ボタンをクリック ← ブログ作成はされないはず
    page.get_by_test_id("blogcreate-submit-btn").click()

    # バリデーションエラーになるはずなので、メッセージがでているかの検証
    expect(page.get_by_test_id("blogcreate-input-title-error")).to_be_visible()
    # エラーメッセージの内容を検証
    expect(page.get_by_text("タイトルは200文字以内で入力してください")).to_be_visible()
    # 本文の入力欄についてのバリデーションエラーはでていないはず
    expect(page.get_by_test_id("bblogcreate-textarea-contents-text-error")).not_to_be_visible()