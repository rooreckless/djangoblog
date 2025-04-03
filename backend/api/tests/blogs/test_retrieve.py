import pytest
from api.models.blogs import Blog
# テストデータの作成用factory
from api.tests.factories.blogFactory import BlogFactory

def test_return_correct_data(db, api_client):
    """正常系"""
        
    #ファクトリーからデータを生成
    blog = BlogFactory()
    # blogの詳細apiにアクセス (アクセス先は、さっきファクトリーで作ったblogのid)
    response = api_client.get(f"/api/v1/blogs/{blog.id}/")
    
    # 詳細apiから200okでかえるはず
    assert response.status_code == 200
    # 詳細apiからの帰りの内、「内容」を取得
    data = response.json()
    # 内容からblogのidやtitle,blogの本文は、ファクトリーから作成したものと一致するはずなので確認
    assert data["id"] == blog.id
    assert data["title"] == blog.title
    assert data["contents_text"] == blog.contents_text

    #--テストケース実行後は、作成したデータ自体は削除される(idの巻き戻しはされないけど)

def test_return_error_with_non_exist_data(db, api_client):
    """エラー系"""
    # 1つもBlogがない状態で、詳細apiを実行してもエラーになるはず
    response = api_client.get("/api/v1/blogs/999/")
    assert response.status_code == 404

    # 1つだけBlogが存在する状態でも、存在しないBlogの詳細apiを実行してもエラーになるはず
    blog = BlogFactory()
    response = api_client.get(f"/api/v1/blogs/{blog.id+1}/")
    assert response.status_code == 404
    