# 作成日と更新日は、大体どのモデルでも使いたいので、抽象基底クラス(Meta abstract True)として定義
# = このモデルはテーブルとして作成されない
from django.db import models


class TimeStampedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True