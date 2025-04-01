from django.db.models import BooleanField, Case, Count, F, Q, Value, When
from api.models.blogs import Blog
# class BlogListQuery:
#     # 共通処理
#     def __init__(
#         self,
#         search: str = "",
#     ):
#         self.__search = search
#         # self.__sort_key = sort_key

#     def __common_q(self):
#         return Blog.objects.filter()

#     def __values(self, q):
#         return q.values(
#             "id",
#             "title",
#             "contents_text",
#             "created",
#             "modified"
#         )

#     def __sort(self, query):
#         return query.order_by(self.__sort_key, "id")

#     def __build_table(self):
#         query = self.__common_q()
#         # return self.__sort(query)
#         return query
#     def table_values(self):
#         return self.__values(self.__build_table())

class BlogQueryService:
    
    def __init__(self, validated_data: dict):
        # Viewから渡される、バリデーション済みのクエリパラメータ
        self.validated_data = validated_data
    
    def get_queryset(self):
        # 初期クエリセット（デフォルトの並び順なし）
        queryset = Blog.objects.all().order_by()
        # タイトルによる部分一致フィルター（case insensitive）
        title = self.validated_data.get('title')
        if title:
            queryset = queryset.filter(title__icontains=title)
        # 本文による部分一致フィルター
        keyword = self.validated_data.get('keyword')
        if keyword:
            queryset = queryset.filter(contents_text__icontains=keyword)
        # ソート条件（例：?sort=-created）
        sort = self.validated_data.get("sort")
        
        
        # ✅ sort の適用（指定があれば）
        if sort:
            # ソートの基準になるフィールドを限定（セキュリティ対策）
            allowed_fields = {"id", "created", "modified"}
            field = sort.lstrip("-")
            if field in allowed_fields:
                queryset = queryset.order_by(sort)
        return queryset