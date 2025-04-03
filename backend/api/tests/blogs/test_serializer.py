import pytest
from api.blog.serializers import BlogRequestSerializer

# 正常系テスト：すべてのパラメータが正しいとき
def test_valid_request_serializer_all_fields():
    data = {
        "title": "検索用タイトル",
        "keyword": "本文内のキーワード",
        "sort": "-created"
    }
    # リクエストシリアライザにはクエリパラメータをいれるには、data=辞書(=request.query_params)の形でいれる
    serializer = BlogRequestSerializer(data=data)
    # そのクエリパラメータが正常かどうかはシリアライザ.is_valid()で確認できる
    assert serializer.is_valid(), serializer.errors
    assert serializer.validated_data["title"] == "検索用タイトル"
    assert serializer.validated_data["keyword"] == "本文内のキーワード"
    assert serializer.validated_data["sort"] == "-created"

# 異常系テスト：存在しないパラメータが含まれている
def test_invalid_request_serializer_unknown_param():
    data = {
        "titlea": "誤ったパラメータ名"  # "title" ではない
    }
    # つまり ?titlea=誤ったパラメータ名 と入力した状態を作る
    serializer = BlogRequestSerializer(data=data)
    # 誤ったパラメータが入っているなら、エラーになることを確認する
    assert not serializer.is_valid()
    assert "titlea" in serializer.errors

# 異常系テスト：ソート対象にすることが許可されていないフィールドを指定した場合
# つまり ?sort=の値が決められた値以外のものだった場合
def test_invalid_sort_field():
    data = {
        "sort": "-not_allowed_field"
    }
    serializer = BlogRequestSerializer(data=data)
    # 決められたsortに使える値以外が入っているならエラーになることを確認する
    # これでシリアライザのvalidate_sortを実行する
    assert not serializer.is_valid()
    assert "sort" in serializer.errors
