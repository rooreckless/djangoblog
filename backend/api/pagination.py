from rest_framework import pagination as pg
from rest_framework.response import Response


class ListPagination(pg.PageNumberPagination):
    """全ての一覧表示で使うためのページネーションクラス"""
    page_size = 2            # デフォルトの件数
    max_page_size = 100      # 1ページあたりの件数の上限
    page_size_query_param = "size"  # クエリパラメータでは?size=3とかを指定できるようになる

    def get_paginated_response(self, data) -> Response:
        # PageNumberPaginationクラスではget_paginated_responseがあるが、これをオーバーライドしてカスタマイズしている
        # オーバーライド(=カスタマイズ)しないと、count、next previous,results(一覧取得結果)しかでてこなくて、不満だから
        content = {
            "num_of_pages":  self.page.paginator.num_pages,
            "num_of_items": self.page.paginator.count,
            "current_page": self.page.number,
            "num_of_items_per_page": self.get_page_size(self.request),
            "results":  data
        }
        return Response(
            content
        )

