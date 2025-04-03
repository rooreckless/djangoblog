from rest_framework import serializers
from api.models.blogs import Blog


class BlogRequestSerializer(serializers.Serializer):
    # このシリアライザで受け付けるパラメータ(例えばtitleで絞るため、?title=abcなどとブラウザに入力できるようにする)
    title = serializers.CharField(required=False, max_length=255)
    size = serializers.IntegerField(required=False, min_value=1, max_value=100)
    page = serializers.IntegerField(required=False)
    sort = serializers.CharField(required=False)
    keyword = serializers.CharField(required=False, max_length=255)
    def is_valid(self, raise_exception=False):
        # 未定義のパラメータがあればエラーにする
        # 例えば、?titlea=abcなどとブラウザにいれてこのシリアライザを使う場合、エラーになるようにするため、is_validをオーバーライド
        # もしこのis_validのオーバーライドがないと、適当なパラメータで検索をかけても動作してしまう。
        unknown_keys = set(self.initial_data.keys()) - set(self.fields.keys())
        if unknown_keys:
            # シリアライザとして定義していないパラメータがクエリパラメータとして仕込まれていたなら、Falseを返す　= is_valid()の結果がfalseになる
            self._errors = {key: ["Unexpected parameter."] for key in unknown_keys}
            # if raise_exception:
            #     raise serializers.ValidationError(self._errors)
            return False

        return super().is_valid(raise_exception=raise_exception)
    def validate_sort(self, value):
        # このメソッドはis_valid実行時にともに実行される
        # 明示的に実行させる必要はなく、このシリアライザに渡された辞書内のキー名がsortになっているもの値についてバリデーションチェックを実施する
        allowed_fields = {"id", "created", "modified"}
        field = value.lstrip("-")
        if field not in allowed_fields:
            raise serializers.ValidationError(f"'{field}' is not a valid sort field.")
        return value

class BlogResponseSerializer(serializers.ModelSerializer):
    class Meta:
        # Blogモデルのレコードを返すことを意味し、つけるフィールドを指定
        model = Blog
        fields = ['id', 'title', 'contents_text', 'created', 'modified']


# リクエスト用のシリアライザはテストを作成しているけど、現状ではレスポンス用のシリアライザのテストは未作成
# Blogモデルのレコードの内、返す値をフィールドから選んでいるだけだから。
# もし「レスポンス用のシリアライザもテストする必要がある」ときが来るとしたら、それは
# 1. レスポンス用シリアライザの中で、to_representation()やSerializerMethodField()を使いだした時
# 2. レスポンス用シリアライザの中で、外部APIや複雑なロジックで値の加工をしだした場合
# 3. レスポンス用シリアライザで、値の形式変換をしだしたとき (日時のフォーマットを、yyyyMMddhhmmから変更をシリアライザでやりだした時)とか