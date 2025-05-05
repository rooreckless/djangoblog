import pytest,json,os
from playwright.sync_api import Page, Route, Request, expect
from playwright._impl._errors import TimeoutError
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


def handle_blog_create_400(route: Route, request: Request):
    if request.method == "POST" and "/api/v1/blogs/" in request.url:
        route.fulfill(
            status=400,
            content_type="application/json",
            body='{"detail": "作成に失敗しました。"}'
        )
    else:
        route.continue_()
# バリデーションエラー (バックエンドとしては400を返すべきだが、フロント側でバリデーションエラーならばバックエンドへリクエストできないはずなのでなにも返さない)     
def handle_blog_create_invalid_input(route: Route, request: Request):
    if request.method == "POST" and "/api/v1/blogs/" in request.url:
        route.fulfill(
            status=400,
            content_type="application/json",
            # body=json.dumps({
            #     "title": ["この項目は空にできません。"],
            #     "contents_text": ["この項目は空にできません。"]
            # })
            body=None
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
    base_url = os.environ.get("BASE_URL")
    # ブログ作成api(のモック)を準備: POST /api/v1/blogs/ に対して成功レスポンスを返す
    page.route("**/api/v1/blogs/", handle_blog_create_201)

    # フロントエンドの作成画面へ遷移
    # page.goto("http://frontend:5173/blogs/create")
    # page.goto('http://front_nginx/blogs/create')
    page.goto(f"{base_url}/blogs/create")

    # 入力フォームにデータを入力
    page.get_by_test_id("blogcreate-input-title").fill("モックタイトル")
    page.get_by_test_id("blogcreate-textarea-contents-text").fill("モック本文")

    # 送信ボタンをクリック ← ブログが作成されたはず
    page.get_by_test_id("blogcreate-back-btn").click()

    # 成功した場合の挙動を検証 = ブログ一覧ページに戻っているはず
    # expect(page).to_have_url("http://frontend:5173/blogs")
    # expect(page).to_have_url("http://front_nginx/blogs")
    expect(page).to_have_url(f"{base_url}/blogs")



def test_blog_create_success_request_response(page: Page):
    """バックエンドからのリクエストとレスポンスを検証し、その内容からフロントエンドの挙動を確認する"""
    base_url = os.environ.get("BASE_URL")
    # ブログ作成apiのモックを準備(正常系)
    page.route("**/api/v1/blogs/", handle_blog_create_201)
    # ブログ作成ページへ遷移
    # page.goto("http://frontend:5173/blogs/create")
    # page.goto('http://front_nginx/blogs/create')
    page.goto(f"{base_url}/blogs/create")

    # フォームに入力
    page.get_by_test_id("blogcreate-input-title").fill("モックタイトル")
    page.get_by_test_id("blogcreate-textarea-contents-text").fill("モック本文")

    # ブログ作成apiへpostリクエスト → その結果のレスポンスをキャッチ
    # with page.expect_response("**/api/v1/blogs/") as response_info:

    # ↓はリクエストもレスポンスも両方とも受けとることができる書き方
    with page.expect_request("**/api/v1/blogs/") as request_info, \
        page.expect_response("**/api/v1/blogs/") as response_info:
        # 作成ボタンをクリック
        page.get_by_test_id("blogcreate-submit-btn").click()
    # リクエストオブジェクト取得
    request = request_info.value
    # リクエストメソッドはPOSTのはず
    assert request.method == "POST"
    # レスポンスオブジェクト取得
    response = response_info.value
    # レスポンスのステータスコードは201のはず
    assert response.status == 201
    # レスポンスのJSONの中身を取得
    data = response.json()
    # レスポンスの内容を確認すす ブログ作成が成功しているので、作成されたブログの情報が返ってくるはず
    assert data["id"] == 1
    assert data["title"] == "モックタイトル"
    assert data["contents_text"] == "モック本文"
    # ブログ一覧ページに遷移していることを確認する
    # expect(page).to_have_url("http://frontend:5173/blogs")
    # expect(page).to_have_url("http://front_nginx/blogs")
    expect(page).to_have_url(f"{base_url}/blogs")
    expect(page.get_by_test_id("bloglist-section-title")).to_have_text("ブログ一覧")
    # ブログ作成画面のエラーメッセージは表示されていないはず。
    expect(page.get_by_test_id("blogcreate-backend-error-message")).not_to_be_visible()


def test_blog_create_with_invalid_input(page: Page):
    """バリデーションエラー タイトル、本文ともに入力しない場合"""
    base_url = os.environ.get("BASE_URL")
    # このテストケースではブログ作成apiのモックをしてもしなくても結果が変わらないが一応準備
    page.route("**/api/v1/blogs/", handle_blog_create_invalid_input)
    # page.goto("http://frontend:5173/blogs/create")
    # page.goto('http://front_nginx/blogs/create')
    page.goto(f"{base_url}/blogs/create")

    # 何も入力しない状態だと送信ボタンをクリックできないはず
    # page.get_by_test_id("blogcreate-submit-btn").click()
    expect( page.get_by_test_id("blogcreate-submit-btn")).to_be_disabled()


def test_create_blog_with_title_too_long(page: Page):
    """バリデーションエラー タイトルの文字列が長すぎる場合"""
    base_url = os.environ.get("BASE_URL")
    # このテストケースではブログ作成apiのモックをしてもしなくても結果が変わらないが一応準備
    page.route("**/api/v1/blogs/", handle_blog_create_201)
    # page.goto("http://frontend:5173/blogs/create")
    # page.goto('http://front_nginx/blogs/create')
    page.goto(f"{base_url}/blogs/create")

    # 201文字のタイトルを入力
    long_title = "あ" * 201
    page.get_by_test_id("blogcreate-input-title").fill(long_title)

    # 本文は正常値を入力
    page.get_by_test_id("blogcreate-textarea-contents-text").fill("本文の内容")

    # # 送信ボタンをクリック ← ブログ作成はされないはず
    # page.get_by_test_id("blogcreate-submit-btn").click()

    # バックエンドへのfetchリクエストが送られないことを確認
    with pytest.raises(TimeoutError):
        with page.expect_request("**/api/v1/blogs/", timeout=1000):
            # ここの部分ではas request_infoを使うことはできない
            # ↓で作成ボタンを押しても、フロントバリデーションエラーが発生中はボタンを押してもリクエストが発生しないから。
            page.get_by_test_id("blogcreate-submit-btn").click()

    # バリデーションエラーになるはずなので、メッセージがでているかの検証
    expect(page.get_by_test_id("blogcreate-input-title-error")).to_be_visible()
    # エラーメッセージの内容を検証
    expect(page.get_by_test_id("blogcreate-input-title-error")).to_have_text("タイトルは200文字以内で入力してください")
    # 本文の入力欄についてのバリデーションエラーはでていないはず
    expect(page.get_by_test_id("bblogcreate-textarea-contents-text-error")).not_to_be_visible()



def test_blog_create_request_payload(page: Page):
    """バリデーションエラー タイトルの文字列が長すぎる場合"""
    base_url = os.environ.get("BASE_URL")
    # このテストケースではブログ作成apiのモックをしてもしなくても結果が変わらないが一応準備
    page.route("**/api/v1/blogs/", handle_blog_create_201)
    # page.goto("http://frontend:5173/blogs/create")
    # page.goto('http://front_nginx/blogs/create')
    page.goto(f"{base_url}/blogs/create")
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
    (handle_blog_create_400, "作成に失敗しました。", 400),
    (handle_blog_create_500, "Internal Server Error", 500),
])
def test_blog_create_failedcase_response_data(page: Page,handler, error_message, expect_backend_status):
    """バックエンドからのエラーレスポンスが帰ってきた時のフロントエンドの挙動を確認する"""
    base_url = os.environ.get("BASE_URL")
    page.route("**/api/v1/blogs/", handler)

    # page.goto("http://frontend:5173/blogs/create")
    # page.goto('http://front_nginx/blogs/create')
    page.goto(f"{base_url}/blogs/create")

    # 入力
    page.get_by_test_id("blogcreate-input-title").fill("テストタイトル")
    page.get_by_test_id("blogcreate-textarea-contents-text").fill("テスト本文")

    # ブログ作成apiへpostリクエスト → その結果のレスポンスをキャッチ
    # with page.expect_response("**/api/v1/blogs/") as response_info:

    # ↓はリクエストもレスポンスも両方とも受けとることができる書き方
    with page.expect_request("**/api/v1/blogs/") as request_info, \
        page.expect_response("**/api/v1/blogs/") as response_info:
        # 送信ボタンをクリック
        page.get_by_test_id("blogcreate-submit-btn").click()
    
    # レスポンスオブジェクト取得
    response = response_info.value
    # ステータスコード確認(= mockのエラーレスポンスが返ってくるはず)
    assert response.status == expect_backend_status
    # JSONレスポンスの中身確認
    data = response.json()
    if expect_backend_status == 400:
        # エラーメッセージが表示されるか確認
        expect(page.get_by_test_id("blogcreate-backend-error-message")).to_be_visible()
        # 400エラー時のレスポンス確認
        assert data["detail"] == error_message       
        # エラーメッセージの内容を確認
        expect(page.get_by_test_id("blogcreate-backend-error-message")).to_have_text(error_message)
    elif expect_backend_status == 500:
        # エラーメッセージが表示されるか確認
        expect(page.get_by_test_id("blogcreate-backend-error-message")).to_be_visible()
        # サーバーエラー=500エラー時のレスポンス確認
        assert data["detail"] == error_message
        # エラーメッセージの内容を確認
        expect(page.get_by_test_id("blogcreate-backend-error-message")).to_have_text(error_message)        


# 他にも　403（認可エラー）や 401（認証エラー）などのケースも考えられるが、今回は省略

# 500エラーになるケースは、はdocker compose -f local.yml stop backendしてから、フロント側で正常にブログ作成をした場合、
# POST http://localhost:8000/api/v1/blogs/ net::ERR_CONNECTION_REFUSED がフロントコンソールにでる
# 一方バックエンドは起動していてもBlogViewSetクラスのcreateメソッドがraise Exceptionするだけだった場合でも起こすことができる
# その場合は、 POST http://localhost:8000/api/v1/blogs/ 500 (Internal Server Error) がフロントコンソールにでる
# どっちの場合でもフロントのBlogCcreate.vueのsubmitBlogメソッドのcatchブロックに入るので、errorMessage.valueに値が入る

# 400エラーは、ブラウザからバックエンドに直接ブログ作成リクエストする際、不要なフィールドを含めてPOSTすると発生する(non_field_errorsが入っているレスポンス)
# 単にフロントエンドで入力必須な欄を未記入にしてPOSTするだけでは、フロントバリデーションエラーで止まるだけ(=リクエスト自体が発生しない)。