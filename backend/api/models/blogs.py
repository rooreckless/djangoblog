# モデル
from django.db import models
# created_a
from .generic.timestamp import TimeStampedModel


class Blog(TimeStampedModel):
    title = models.CharField(verbose_name='title', blank=False, null=False, max_length=255)
    contents_text = models.TextField(
        verbose_name='contents_text',
        blank=True,
        null=True,
        max_length=1000,
    )
    def __str__(self):
        return self.title

# --- 現状ではこのモデルのテストケースは作成していない
# 理由は、
# 「単純なデータ構造のみ」
# 「モデル自体でバリデーションを実施していない」
# 「リレーションがなかったりあっても単純」から
#-----
# もしモデルのテストを作成する必要があるとしたら
# 1. 独自のメソッドや、プロパティをモデルで定義しだした時
# 2. clean()をオーバーライドし、独自のバリデーションをしているとき
# 3. save()をオーバーライドし、レコードを保存する前や後に何等かの処理を追加しだしたとき