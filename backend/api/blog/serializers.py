from rest_framework import serializers
from api.models.blogs import Blog


class BlogRequestSerializer(serializers.Serializer):
    # Blog一覧APIへのリクエストを受け付けるシリアライザ
    # このシリアライザで受け付けるパラメータ(例えばtitleで絞るため、?title=abcなどとブラウザに入力できるようにする)
    title = serializers.CharField(required=False, max_length=255,label="タイトル",
        help_text="検索による絞り込み用にタイトルを入力してください")
    size = serializers.IntegerField(required=False, min_value=1, max_value=100)
    page = serializers.IntegerField(required=False)
    sort = serializers.CharField(required=False)
    keyword = serializers.CharField(required=False, max_length=255)

    def validate(self, attrs):
        # 未定義のパラメータ(unknown_keys)があればエラーにする
        # 例えば、?titlea=abcなどとブラウザにいれてこのシリアライザを使う場合、エラーになるようにするため、is_validをオーバーライド
        # もしこのis_validのオーバーライドがないと、適当なパラメータで検索をかけても動作してしまう。
        print("---attrs", attrs)
        print("---self.initial_data", self.initial_data)
        unknown_keys = set(self.initial_data.keys()) - set(self.fields.keys())
        if unknown_keys:
            # シリアライザとして定義していないパラメータがクエリパラメータとして仕込まれていた(unknown_keysがある)なら、serializers.ValidationErrorを返す
            raise serializers.ValidationError({
                key: ["Unexpected parameter."] for key in unknown_keys
            })
        return attrs
    def validate_sort(self, value):
        # このメソッドはis_valid実行時にともに実行される
        # 明示的に実行させる必要はなく、このシリアライザに渡された辞書内のキー名がsortになっているもの値についてバリデーションチェックを実施する
        allowed_fields = {"id", "created", "modified"}
        field = value.lstrip("-")
        if field not in allowed_fields:
            raise serializers.ValidationError(f"'{field}' is not a valid sort field.")
        return value

class BlogResponseSerializer(serializers.ModelSerializer):
    # Blogモデルのレコードを返すためのシリアライザ
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

class BlogCreateRequestSerializer(serializers.Serializer):
    title = serializers.CharField(required=True, max_length=200,label="タイトル",
        help_text="検索による絞り込み用にタイトルを入力してください")
    contents_text = serializers.CharField(required=True,)
    class Meta:
        model = Blog
        # このシリアライザで受けるキーを限定。「これら以外がくるとエラーになるようにする」のがvalidateメソッドの話。
        fields = ("title", "contents_text")

    def validate(self, attrs):
        # リクエストの全体データをチェック
        request_data_keys = set(self.initial_data.keys())
        allowed_keys = set(self.fields.keys())

        # 許可されていないキー(=フィールド)が含まれているか
        extra_keys = request_data_keys - allowed_keys
        if extra_keys:
            raise serializers.ValidationError(f"不正なフィールドが含まれています: {', '.join(extra_keys)}")

        return attrs

#----
# リクエストシリアライザ内のis_validメソッドのオーバーライドをやめて、validateメソッドのオーバーライドにした理由
# メソッド	主な用途	呼び出されるタイミング	適した処理
# is_valid()	全体のバリデーション処理を起動	呼び出し時に1度だけ	通常は上書きしない
# validate()	全フィールドを検査（cross-field含む）	is_valid() の中で呼ばれる	今回のような全体検査
# validate_<field>()	単一フィールドの検証	各フィールド処理時	個別の条件検証