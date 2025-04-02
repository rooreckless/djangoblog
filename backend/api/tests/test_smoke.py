# このテストケースファイルは、テストケースの作り方の説明のために配置しています。
# 後日削除します。
import pytest
from api.models.blogs import Blog

# # 以下は古いテストケース(Factoryによるテスト用データの事前作成をせず、テスト中に作成するやり方)
# テストケースの定義方法は以下2通りのどれかを使えばいい

# 1 @pytest.mark.django_dbをデコレータとしてつける(@pytest.fixtureをデコレータにしても一緒)
from rest_framework.test import APIClient
@pytest.mark.django_db
def test_blog_list_return_default_nouse_factory():
    # データを3件作成(Factoryはつかわず)
    blog1 = Blog.objects.create(title="Title1", contents_text="Content1")
    blog2 = Blog.objects.create(title="Title2", contents_text="Content2")
    blog3 = Blog.objects.create(title="Title3", contents_text="Content3")

    client = APIClient()
    # blog一覧apiを実行してレスポンスを得る
    response = client.get(f"/api/v1/blogs/")
    # レスポンスが正しく帰ってきているかを確認する
    assert response.status_code == 200
    data = response.json()
    assert data["num_of_items"] == 3
    assert len(data["results"]) == 3

    # ---テストケースが終了したら、そのテストケースでcreateしたblogは消えている(idは巻き戻らないけど) ---

# 2 テストケースの引数にdbをいれる(インポートしなくてもいい) transactional_dbを入れるでも一緒
def test_blog_retrieve_return_default_nouse_factory(db):
    # 詳細api用
    # データを1件作成(Factoryはつかわず)
    blog1 = Blog.objects.create(title="Title1", contents_text="Content1")
    
    client = APIClient()
    # blog詳細apiを実行してレスポンスを得る
    response = client.get(f"/api/v1/blogs/{blog1.id}/")
    # レスポンスが正しく帰ってきているかを確認する
    assert response.status_code == 200
    data = response.json()
    # 内容からblogのidやtitle,blogの本文は、ファクトリーから作成したものと一致するはずなので確認
    assert data["id"] == blog1.id
    assert data["title"] == blog1.title
    assert data["contents_text"] == blog1.contents_text


# Factoryでテスト用のデータを作成させ、それをもとにテストをする場合などは、backend/api/tests/blogsのtest_~.pyを参照