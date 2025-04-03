import pytest
from api.blog.query import BlogQueryService
from api.models.blogs import Blog
from api.tests.factories.blogFactory import BlogFactory  # FactoryBoyを使ってる前提

# このファイルの目的：
# BlogQueryService は、APIのリクエストパラメータに応じて、
# Blogモデルの絞り込み・並び替えを行う責任を持つサービスクラス。
# そのロジックが正しく動いているかを確認するためのテスト。


def test_query_service_filters_by_title(db):
    """
    タイトルに "Django" を含むものだけが検索されるか確認
    """
    # Factory を使ってテスト用の Blog を3件生成（DBに保存）
    BlogFactory(title="Django入門")
    BlogFactory(title="Vue.jsガイド")
    BlogFactory(title="Django REST Framework")

    # クエリのクラスに検索条件を、辞書で渡してインスタンスを作成 = 検索条件が指定された状態
    # 今回は、「title に "Django" が含まれるものだけ」という条件(フィルタリング)
    service = BlogQueryService({"title": "Django"})
    # get_queryset()を実行した返り値は検索結果 = 検索が実行された状態
    # だが返り値はQuerySetのインスタンス
    qs = service.get_queryset()
    # 検索結果から、titleだけを抜き出す
    # 1. まずqsだけでは、<QuerySet>オブジェクト
    # 2. list(qs)だと、[Blogオブジェクト, Blogオブジェクト] ← 検索結果は複数になるのだから当然リスト内にblogオブジェクト
    # 3. list(qs.values_list("title"))だと、[(Blogオブジェクトのtitle), (Blogオブジェクトのtitle)]
    # https://zenn.dev/kumamoto/scraps/45bc3f36006189
    # https://docs.djangoproject.com/ja/5.2/ref/models/querysets/#values-list
    # 4. list(qs.values_list("title",flat=True))だと、[Blogオブジェクトのtitle, Blogオブジェクトのtitle]
    # よって以下のtitlesは、4の「クエリによる検索結果のタイトルの値だけを並べたリスト」になる。
    # これでassertしていく
    titles = list(qs.values_list("title", flat=True))
    
    # 検索結果は2件のはず
    assert len(titles) == 2
    # 検索結果の中に「Django」が含まれている2があるはず
    assert "Django入門" in titles
    assert "Django REST Framework" in titles
    # 「Django」がふくまれていないものは、検索結果にないはず
    assert "Vue.jsガイド" not in titles
    # 【余談】qsから、フィールド名のリストを出すこともできるが、それは [f.name for f in qs.model._meta.fields]
def test_query_service_filters_by_keyword(db):
    """
    本文（contents_text）に "Django" を含む記事だけが返るかを確認
    """
    # このテストケースでやってることは↑とほぼ一緒なので省略
    BlogFactory(contents_text="PythonとDjangoの解説")
    BlogFactory(contents_text="Vue.jsはフロントエンド")
    BlogFactory(contents_text="DjangoのAPIの作り方")

    service = BlogQueryService({"keyword": "Django"})
    qs = service.get_queryset()

    contents = list(qs.values_list("contents_text", flat=True))
    assert len(contents) == 2
    assert all("Django" in content for content in contents)


def test_query_service_applies_sort(db):
    """
    created フィールドで並び替えが正しくできるかを確認
    """
    blog1 = BlogFactory(title="古い記事")
    blog2 = BlogFactory(title="新しい記事")

    # `created` が明確に異なるようにするため、save順序を保証
    # blog1の方がblog2より1年古く作成された状態にしている
    blog1.created = "2022-01-01T00:00:00Z"
    blog1.save()
    blog2.created = "2023-01-01T00:00:00Z"
    blog2.save()

    service = BlogQueryService({"sort": "-created"}) # 降順（新しい順）でBlog一覧を取得
    qs = service.get_queryset()
    results = list(qs)
    # クエリの実行結果は、「新しいものから順」になっているかを確認する
    assert results[0].id == blog2.id
    assert results[1].id == blog1.id
