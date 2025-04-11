from django.core.management.base import BaseCommand
from api.tests.factories.blogFactory import BlogFactory


class Command(BaseCommand):
    help = "ブログのサンプルデータを作成します"

    def add_arguments(self, parser):
        parser.add_argument(
            "--count",
            type=int,
            default=13,
            help="作成するブログ数（デフォルト: 10）",
        )

    def handle(self, *args, **options):
        #---
        # e2eテスト実行前に、用意しておきたいデータはここで登録しておく
        # 以下ではブログオブジェクトをcountの分だけ作成している
        # ただし、e2eテストとしては事前データなしで実行していきたいので、将来的にはこれはなくなるはず。
        #---
        count = options["count"]
        self.stdout.write(f"{count} 件のブログを作成します...")
        BlogFactory.create_batch(count)
        self.stdout.write(self.style.SUCCESS("サンプルデータ作成完了 ✅"))