# backend/api/tests/factories.py
import factory
from api.models.blogs import Blog
# Blogモデルのデータを作るためにやること
# https://qiita.com/shun198/items/80bd2a79e483e7a72c6d#factory_boy%E3%81%AE%E4%BD%9C%E6%88%90%E6%96%B9%E6%B3%95
# 1. Blogモデルとfactoryのインポート
# 2. factory.django.DjangoModelFactoryを継承したクラスを定義
# 3. 2の中でclass Metaを定義、そのMetaクラスではmodel 変数に対象のモデルクラス名(今回はBlog)
# 4. あとはBlogFactoryの属性をみたらわかりやすいはず
class BlogFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Blog
    # Blogモデルのレコードを作る際、自力での入力が必要な列については以下のように列名のフィールド定義が必要
    # factory.Fakerはランダムな文字列を作成するのに使用する
    # sentenceで「短めの文章」で、nb_words=4は「4単語でつくる」の意味
    title = factory.Faker("sentence", nb_words=4)
    # textが引数になっていると通常文字列だが、max_nb_chars=1000で「最大で1000文字までの長さ」になる
    contents_text = factory.Faker("text", max_nb_chars=1000)
