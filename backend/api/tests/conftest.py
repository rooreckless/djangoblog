# backend/api/tests/conftest.py

import pytest
from rest_framework.test import APIClient
# このファイルに書かれた@pytest.fixtureの内容は、このファイルが以下のディレクトリにあるtest_~.pyならば、引数にいきなりいれてok(import不要)
# 例えば以下の状態だと、testsディレクトリ以下のtest_~.pyでapi_clientを引数に入れて、api_client()で実行することができる。
# 実行した意味はrest_framework.test.APIClient()と同じになる。
@pytest.fixture
def api_client():
    return APIClient()

# @pytest.fixtureにすべき内容としては、

# 1. logined_userメソッドとか : ログインをしたうえで実行するテストがあるので、ユーザーを作成 -> ログイン状態にして返すメソッド
# そのメソッドがあれば、テストケース内ではいきなりlogined_user()で「ログイン済みユーザー」での操作ができるようになる(テストケースの引数にもいれようね)

# 2. 複数のモデルのデータやそのリレーションを一度に用意し、さらにそれを複数用意する前処理メソッド
# 例えば、ブログとそれに紐づくタグとそのリレーション、さらにユーザーとそのリレーションをあらかじめ作成する場合

# 3. あるモデルのレコードを複数用意する必要がある場合 : 中で、モデル.objects.createを何度も実行したり、モデル.createa_batch()をしたりする
# fixtureの中で、固定のレコードを作成するでもいいし、factory_boyを使ってランダムにレコードを作成してもいい。