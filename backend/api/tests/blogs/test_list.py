import pytest
from api.models.blogs import Blog
# テストデータの作成用factory
from api.tests.factories.blogFactory import BlogFactory


def test_return_default(db, api_client):
    """正常系テスト 30件Blogを登録した状態の一覧APIが返す内容について"""
    # データを30件作成 ファクトリーから30件まとめて作成する
    # BlogFactory.create_batch(30)
    # タイトルや文章も指定して作成したいので以下のやり方で実施する
    for i in range(0, 30):
        BlogFactory(title=f"タイトル_{i}", contents_text=f"コンテンツ_{i}")

    # ページとページごとのデータ件数の指定がない場合、1ページ目で、10件取得できるかを確認する
    response = api_client.get("/api/v1/blogs/")
    assert response.status_code == 200
    data = response.json()
    # 1ページ値のblogの件数はデフォルトでは10のはず
    assert len(data["results"]) == 10
    assert data["num_of_items_per_page"] == 10
    # pageの指定がないなら、1ページ目を取得しているはず
    assert data["current_page"] == 1
    # ページネーションをしていたとしても、総データ数としては30件であるはず
    assert data["num_of_items"] == 30
    # 総ページ数は3ページのはず(1ページあたり10件で総件数30件だから、3ページ)
    assert data["num_of_pages"] == 3
    
    # results の中身も簡単にチェック (Factoryで作成したものと一致するはず)
    for i, blog in enumerate(data["results"]):
        reversed_i = data["num_of_items"]- 1 - i
        # titleの内容は タイトル_29,タイトル_28 ～ タイトル20のはず
        assert blog["title"] == f"タイトル_{reversed_i}"
        # contents_textの内容も同様のはず
        assert blog["contents_text"] == f"コンテンツ_{reversed_i}"

def test_return_page_size(db, api_client):
    """正常系テスト pageとsizeを指定したときの一覧APIの返す内容について"""
    # データを30件作成 ファクトリーから30件まとめて作成する
    BlogFactory.create_batch(30)

    # ページとページごとのデータ件数の指定をしたときの一覧APIの結果を確認する
    # 今回はページごとのデータ数は3にして2ページ目を取得する
    response = api_client.get("/api/v1/blogs/?size=3&page=2")
    assert response.status_code == 200
    data = response.json()
    print("---data=",data)
    # apiの出力の内resultsの長さは3(=size)のはず
    assert len(data["results"]) == 3
    assert data["current_page"] == 2
    # ページネーションをしていたとしても、総データ数としては30件であるはず
    assert data["num_of_items"] == 30
    # 総ページ数は3ページのはず(1ページあたり3件で総件数30件だから、3ページ)
    assert data["num_of_pages"] == 10

def test_error_by_over_max_page_size(db, api_client):
    """エラー系 sizeがmax_page_sizeを超えているケース"""
    # データを200件作成 ファクトリーから200件まとめて作成する
    BlogFactory.create_batch(200)

    # ページとページごとのデータ件数の指定をしたときの一覧APIの結果を確認する
    # 今回はページごとのデータ数は101(max_page_sizeの100を超えている)にし、1ページ目を取得する
    response = api_client.get("/api/v1/blogs/?size=101&page=1")
    # エラーがかえってくるはず
    assert response.status_code == 400
    data = response.json()
    # 帰ってきた内容(エラーの内容)を確認する
    assert data["message"] == "パラメータが不正です。"
    assert data["errors"]["size"][0] == "この値は100以下にしてください。"


def test_error_by_over_max_page_size(db, api_client):
    """エラー系 pageがnum_of_pageを超えているケース"""
    # データを30件作成 ファクトリーから30件まとめて作成する
    BlogFactory.create_batch(30)

    # ページとページごとのデータ件数の指定をしたときの一覧APIの結果を確認する
    
    # sizeを指定しないデフォルトでは1ページごとの件数は10なので、4ページ目を取得しようとするとエラーのはず
    response = api_client.get("/api/v1/blogs/?page=4")
    # エラーがかえってくるはず
    assert response.status_code == 404
    data = response.json()
    # 帰ってきた内容(エラーの内容)を確認する
    assert data["detail"] == "不正なページです。"

def test_error_by_over_max_page_size(db, api_client):
    """正常系 pageとsizeを適切に設定しているケース"""
    # データを30件作成 ファクトリーから30件まとめて作成する
    BlogFactory.create_batch(30)

    # size=1もpage=4も指定して一覧を取得
    response = api_client.get("/api/v1/blogs/?size=1&page=4")
    # エラーにならないはず
    assert response.status_code == 200
    
    data = response.json()
    # 1ページあたりのデータ件数は1件 == size のはず
    assert len(data["results"]) == 1
    # 現在は4ページ目にいるはず
    assert data["current_page"] == 4
    # ページネーションをしていたとしても、総データ数としては30件であるはず
    assert data["num_of_items"] == 30
    # 総ページ数は30ページのはず(1ページあたり1件で総件数30件だから、30ページ)
    assert data["num_of_pages"] == 30