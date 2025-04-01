# 共通で使うシリアライザ　エラー関連
from rest_framework import serializers

class ErrorResponseSerializer(serializers.Serializer):
    status = serializers.IntegerField()
    code = serializers.IntegerField()
    message = serializers.CharField()

# このクラスを継承してシリアライザを作成すればいい
class ValidationErrorResponseSerializer(ErrorResponseSerializer):
    errors = serializers.DictField(help_text="キーがエラーであるパラメータに対応した辞書")