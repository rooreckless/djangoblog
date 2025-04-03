from django.core.management.base import BaseCommand
from api.tests.factories.blogFactory import BlogFactory


class Command(BaseCommand):
    help = "ブログのサンプルデータを作成します"

    def add_arguments(self, parser):
        parser.add_argument(
            "--count",
            type=int,
            default=10,
            help="作成するブログ数（デフォルト: 10）",
        )

    def handle(self, *args, **options):
        count = options["count"]
        self.stdout.write(f"{count} 件のブログを作成します...")
        BlogFactory.create_batch(count)
        self.stdout.write(self.style.SUCCESS("サンプルデータ作成完了 ✅"))