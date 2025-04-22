import pytest
from playwright.sync_api import Page, Route, Request, expect

#---バックエンドのモック---
# 正常系なブログ作成用モック
def handle_blog_create_201(route: Route, request: Request):
    if request.method == "POST" and "/api/v1/blogs/" in request.url:
        route.fulfill(
            status=201,
            content_type="application/json",
            body='{"id": 1, "title": "モックタイトル", "contents_text": "モック本文"}'
        )
    else:
        route.continue_()

# バリデーションエラー: 400)
def handle_blog_create_400(route: Route, request: Request):
    if request.method == "POST" and "/api/v1/blogs/" in request.url:
        route.fulfill(
            status=400,
            content_type="application/json",
            body='{"detail": "エラーが発生しました"}'
        )
    else:
        route.continue_()
# サーバーエラー: 500
def handle_blog_create_500(route: Route, request: Request):
    if request.method == "POST" and "/api/v1/blogs/" in request.url:
        route.fulfill(
            status=500,
            content_type="application/json",
            body='{"detail": "Internal Server Error"}'
        )
    else:
        route.continue_()

#---テストケース---
def test_create_blog_success(page: Page):
    """正常系"""
    # ブログ作成api(のモック)を準備: POST /api/v1/blogs/ に対して成功レスポンスを返す
    page.route("**/api/v1/blogs/", handle_blog_create_201)

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
    """バリデーションエラー タイトル、本文ともに入力しない場合"""
    # このテストケースではブログ作成apiのモックをしてもしなくても結果が変わらないが一応準備
    page.route("**/api/v1/blogs/", handle_blog_create_201)
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
    """バリデーションエラー タイトルの文字列が長すぎる場合"""
    # このテストケースではブログ作成apiのモックをしてもしなくても結果が変わらないが一応準備
    page.route("**/api/v1/blogs/", handle_blog_create_201)
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
    expect(page.get_by_test_id("blogcreate-input-title-error")).to_have_text("タイトルは200文字以内で入力してください")
    # 本文の入力欄についてのバリデーションエラーはでていないはず
    expect(page.get_by_test_id("bblogcreate-textarea-contents-text-error")).not_to_be_visible()



def test_blog_create_request_payload(page: Page):
    """バリデーションエラー タイトルの文字列が長すぎる場合"""
    # このテストケースではブログ作成apiのモックをしてもしなくても結果が変わらないが一応準備
    page.route("**/api/v1/blogs/", handle_blog_create_201)
    page.goto("http://frontend:5173/blogs/create")

    # フィールドに値を入力
    page.get_by_test_id("blogcreate-input-title").fill("テストタイトル")
    page.get_by_test_id("blogcreate-textarea-contents-text").fill("テスト本文")

    # POST リクエストを実施する
    with page.expect_request("**/api/v1/blogs/") as intercepted_request:
        page.get_by_test_id("blogcreate-submit-btn").click()

    request_obj = intercepted_request.value
    # POSTリクエストが行われた ことを確認
    assert request_obj.method == "POST"

    # リクエストのボディの内容を検証
    assert request_obj.post_data_json == {
        "title": "テストタイトル",
        "contents_text": "テスト本文"
    }

@pytest.mark.parametrize("handler,error_message,expect_backend_status", [
    (handle_blog_create_201, "", 201),
    (handle_blog_create_400, "エラーが発生しました", 400),
    (handle_blog_create_500, "Internal Server Error", 500),
])
def test_blog_create_response_data(page: Page, handler, error_message, expect_backend_status):
    """バックエンドからのレスポンスを検証し、その内容からフロントエンドの挙動を確認する"""
    page.route("**/api/v1/blogs/", handler)

    page.goto("http://frontend:5173/blogs/create")

    # 入力
    page.get_by_test_id("blogcreate-input-title").fill("テストタイトル")
    page.get_by_test_id("blogcreate-textarea-contents-text").fill("テスト本文")

    # ブログ作成apiへpostリクエスト → その結果のレスポンスをキャッチ
    with page.expect_response("**/api/v1/blogs/") as response_info:
        # 送信ボタンをクリック
        page.get_by_test_id("blogcreate-submit-btn").click()
    
    # レスポンスオブジェクト取得
    response = response_info.value
    # ステータスコード確認
    assert response.status == expect_backend_status
    # JSONレスポンスの中身確認
    data = response.json()
    if expect_backend_status == 201:
        # 成功時のレスポンス確認
        assert data["id"] == 1
        assert data["title"] == "モックタイトル"
        assert data["contents_text"] == "モック本文"
    elif expect_backend_status == 400:
        # エラーメッセージが表示されるか確認
        expect(page.get_by_test_id("blogcreate-backend-error-message")).to_be_visible()
        # 400エラー時のレスポンス確認
        assert data["detail"] == "エラーが発生しました"
        # エラーメッセージの内容を確認
        expect(page.get_by_test_id("blogcreate-backend-error-message")).to_have_text(error_message)
    elif expect_backend_status == 500:
        # エラーメッセージが表示されるか確認
        expect(page.get_by_test_id("blogcreate-backend-error-message")).to_be_visible()
        # サーバーエラー=500エラー時のレスポンス確認
        assert data["detail"] == "Internal Server Error"
        # エラーメッセージの内容を確認
        expect(page.get_by_test_id("blogcreate-backend-error-message")).to_have_text(error_message)        



