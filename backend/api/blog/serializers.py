from rest_framework import serializers
from api.models.blogs import Blog



# class BlogListRequestSerializer(serializers.Serializer):
#     # page = serializers.IntegerField(min_value=1)
#     # size = serializers.ChoiceField(choices=[(int(s), int(s))
#     #                                for s in PageSize], help_text="ページあたりの項目数")
#     search = serializers.CharField(default="", max_length=200)


class BlogRequestSerializer(serializers.Serializer):
    # このシリアライザで受け付けるパラメータ(例えばtitleで絞るため、?title=abcなどとブラウザに入力できるようにする)
    title = serializers.CharField(required=False, max_length=255)
    size = serializers.IntegerField(required=False, min_value=1, max_value=100)
    page = serializers.IntegerField(required=False)
    sort = serializers.CharField(required=False)
    # keyword = serializers.CharField(required=False, max_length=255)
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

class BlogResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ['id', 'title', 'contents_text', 'created', 'modified']