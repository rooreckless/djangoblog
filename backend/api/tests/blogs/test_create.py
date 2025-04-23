import pytest
from rest_framework.test import APIClient
from rest_framework import status
from api.models.blogs import Blog

# クラス内の各テストケースで使うことになるAPIClientの準備
# ただし、テストケースメソッドにapi_clientを引数にいれたら、conftest.pyのフィクスチャを使って同じことができる
client = APIClient()

@pytest.fixture
def data_for_blogcreate():
    # ブログ作成APIのテスト用のデータを返す
    return {
        "title": "テストタイトル",
        "contents_text": "テスト本文",
    }



@pytest.mark.django_db
class TestBlogCreateAPI:
    #このクラス内のテストケースメソッドに引数にdbを入れなくても、@pytest.mark.django_dbをつけることで、テストケースメソッド内でテスト用DBを使えるようになる
    # api_clientは、conftest.pyで@pytest.fixtureで定義したフィクスチャ
    # data_for_blogcreateは、同じこのファイルで定義のフィクスチャ (← あまり意味はないが説明のため)
    def test_create_blog_success(self, api_client, data_for_blogcreate):
        """正常系"""
        
        # フィクスチャを使う前は以下のように、ブログ作成に必要なパラメータを「テストケース内で」準備していた
        # data = {
        #     "title": "テストタイトル",
        #     "contents_text": "テスト本文",
        # }
        # フィクスチャを使わない場合以下のようにAPIClientをインスタンスをこのテストケースで作成してpostリクエスト=blog作成していた。
        # response = client.post("/api/v1/blogs/", data, format="json")
        
        # 現在は以下のように、フィクスチャからのAPIClientとパラメータを使ってpost=ブログ作成している。
        response = api_client.post("/api/v1/blogs/", data_for_blogcreate, format="json")
        # ブログ作成時のレスポンスのステータスコードを確認(正常のはず)
        assert response.status_code == status.HTTP_201_CREATED
        
        # レスポンスには、作成時に渡したパラメータが含まれているはず(フィクスチャ未使用版と使用版)
        # assert response.data["title"] == data["title"]
        # assert response.data["contents_text"] == data["contents_text"]
        assert response.data["title"] == data_for_blogcreate["title"]
        assert response.data["contents_text"] == data_for_blogcreate["contents_text"]
        # 作成されたブログは1件だけのはずなので確認する
        assert Blog.objects.count() == 1

    def test_create_blog_missing_title(self):
        """エラー系 ブログ作成時に、本文だけ値があるとエラーになること"""
        data = {
            "contents_text": "本文だけ",
        }
        response = client.post("/api/v1/blogs/", data, format="json")
        # 作成できなかったはずなので、ステータスを確認する(エラーが返ってくるはず)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        # ブログを作成できなかった時のレスポンスには、「titleがパラメータになかったから」が含まれているか
        assert "title" in response.data

    def test_create_blog_missing_contents(self):
        """エラー系 ブログ作成時に、ブログ作成時に、タイトルだけ値があるとエラーになること"""
        data = {
            "title": "タイトルだけ",
        }
        response = client.post("/api/v1/blogs/", data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "contents_text" in response.data

    def test_create_blog_with_unknown_field(self):
        """エラー系 ブログ作成時に、シリアライザが定義していないフィールドへの入力があればエラーになること"""
        
        data = {
            "title": "不正テストのokなタイトル",
            "contents_text": "OKな本文",
            "extra": "これは余計なキー",    # ←ブログ作成に使うシリアライザはextraというキーを想定していない
        }
        response = client.post("/api/v1/blogs/", data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        # ブログ作成リクエスト用シリアライザに、余計なキー(フィールド)があった状態でpostリクエストしたらエラー
        # そのエラーに終わった時のレスポンスにも、エラーの理由として「余計なキーがあったから」を意味するnon_field_errorsが入っているか
        assert "non_field_errors" in response.data
        # レスポンスのnon_field_errorsの内容を確認する
        assert response.data["non_field_errors"][0] == "不正なフィールドが含まれています: extra"
    def test_create_blog_with_invalid_type(self):
        """エラー系 ブログ作成時に、文字列へ変換できない値をapiへ渡した場合エラーになることを確認する"""
        data = {
            "title": False,  # 本来はstrまたはstrにキャストできるものでないと受け付けられない
            "contents_text": True,  # 本来はstrまたはstrにキャストできるものでないと受け付けられない
        }
        response = client.post("/api/v1/blogs/", data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        # ブログを作成できなかった時のレスポンスには、「titleと、contesnts_textそれぞれに問題があったから」となっているかどうか
        assert "title" in response.data
        assert "contents_text" in response.data

# setup_methodやsetup_classを使って個々のテストを実行する前に前処理をすることもできるが、ログインができないと意味が薄いので
# 今はpytest.fixureのみで十分