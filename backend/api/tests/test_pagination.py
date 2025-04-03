import pytest
from api.models.blogs import Blog
from api.tests.factories.blogFactory import BlogFactory

# ページネーションのテストを実施します。
# backend/api/pagination.py::ListPaginationを採用しているViewset共通の内容になるので、Blogモデルを使用してテストしています。

def test_list_pagination_default(db, api_client):
    # 例：12件作成（ページサイズ 5 にして3ページになるはず）
    BlogFactory.create_batch(12)

    response = api_client.get("/api/v1/blogs/?size=5&page=2")
    assert response.status_code == 200

    data = response.json()
    assert "results" in data
    assert len(data["results"]) == 5  # 2ページ目も5件のはず

    assert data["current_page"] == 2
    assert data["num_of_pages"] == 3
    assert data["num_of_items"] == 12
    assert data["num_of_items_per_page"] == 5


def test_list_pagination_request_overpage(db, api_client):
    BlogFactory.create_batch(5)

    response = api_client.get("/api/v1/blogs/?page=99&size=5")
    assert response.status_code == 404

    data = response.json()
    assert data["detail"] == "不正なページです。"


# ----他にもテストできること（応用）----
# get_paginated_response() を直接呼び出すユニットテスト
# max_page_size の制限を超えた場合の挙動
# page_size_query_param に指定されてないときのデフォルト挙動

