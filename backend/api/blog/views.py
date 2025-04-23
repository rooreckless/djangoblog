from rest_framework import viewsets
from api.models.blogs import Blog
from rest_framework import status
from api.pagination import ListPagination
from rest_framework.exceptions import NotFound
from .serializers import BlogRequestSerializer, BlogResponseSerializer, BlogCreateRequestSerializer
from rest_framework.response import Response
from api.serializers import ValidationErrorResponseSerializer
from api.blog.query import BlogQueryService

from drf_spectacular.utils import extend_schema

class BlogViewSet(viewsets.GenericViewSet):
    # GenericViewset以外にModelViewSetを使うこともありだが、違いは https://qiita.com/usayamadausako/items/be70a57a6d24d20a05e3
    pagination_class = ListPagination
    # 以下のserializer_classに指定したシリアライザを必ずしも使うとは限らないけれど、定義しとかないとDRF的にはエラーなので実施
    # 【理由】このBlogViewSetクラスではlistやcreateメソッドなどで、直接シリアライザを扱うことにしているから。
    serializer_class = BlogResponseSerializer
    def get_queryset(self):
        """
        DRFの内部メソッドで使用されるが、今回は未使用。
        list() メソッド内で明示的にクエリセットを扱うため、ここは安全な初期値でOK。
        """
        return 
    # Blog.objects.all()  # ← これでOK！

    @extend_schema(
        summary="ブログ一覧の取得",
        description="フィルター付きでブログ記事を一覧取得します",
        parameters=[BlogRequestSerializer],
        responses={
            200: BlogResponseSerializer,
            400: ValidationErrorResponseSerializer
        }
    )
    def list(self, request):
        # 流れ
        # ①	クエリパラメータをシリアライザに通す & それをバリデーションチェック	BlogRequestSerializer と is_valid()
        # ②	クエリセット構築	BlogQueryService.get_queryset()
        # ③	ページ単位にスライス	ListPagination.paginate_queryset()
        # ④	シリアル化	BlogResponseSerializer
        # ⑤	レスポンス構成	ListPagination.get_paginated_response()

        # ①-1 クエリパラメータをリクエスト用シリアライザに通す
        # ブログ一覧取得APIには、リクエスト用のシリアライザが必要 = 検索で絞ったりする必要がでるから
        request_serializer = BlogRequestSerializer(data=request.query_params)
        # ①-2 クリエパラメータのバリデーションチェックは、リクエスト用シリアライザ単位で実施
        if not request_serializer.is_valid():
            # バリデーションエラーの場合の挙動
            # まずはエラー用のシリアライザを、返す値をつめて作成
            error_response_serializer = ValidationErrorResponseSerializer(data={
                "status": 400,
                "code": 1,
                "message": "パラメータが不正です。",
                "errors": request_serializer.errors
            })
            # エラー用シリアライザとしてもバリデーションは一応チェック
            error_response_serializer.is_valid(raise_exception=True)
            # バリデーションエラー時用のレスポンス
            return Response(data=error_response_serializer.data, status=400)
        # ② リクエストのバリデーションチェックは終わったので、BlogQueryService を使って、検索条件付きクエリセットを取得
        service = BlogQueryService(request_serializer.validated_data)
        # クエリのget_querysetメソッドを明示的に実行 = タイトルでの絞り込みや並び替えをするのがここ
        # 結果はクエリセット(厳密にはまだ、この段階のquerysetは絞り込み結果(SQL実行結果)ではない。SQL準備段階)
        queryset = service.get_queryset()

        # ③ ページネーションを適用(スライス)
        # まずはGenericAPIViewで定義されているpaginate_querysetを使う
        # = pagination_classに指定したクラスのpaginate_queryset()を使う
        # = 継承しているrest_framework.pagination.PageNumberPaginationクラスのpaginate_queryset()を使う
        # そのクラスのpaginate_querysetわたす引数はクエリの実行結果 = 絞り込みを行った結果 を渡すことで、ページネーションを実行する
        page = self.paginate_queryset(queryset) # ← size, page のパラメータを内部で参照　pagination_classに指定したクラスの
        # ↑ちなみに、querysetはこのself.paginate_queryset(queryset)でSQLが評価される。querysetがlist()にラップされて、スライスされるので。
        # なので返り値のpageはリスト

        if page is not None:
            # ④ページ単位でレスポンス用シリアライザに通し、viewとして返す形に整える → カスタムページネーションの形式でレスポンスするということ
            response_serializer = BlogResponseSerializer(page, many=True)
            # ⑤pagination_classに指定したクラスで定義したget_paginated_responseを明示的使い、Responseを行う(selfになっているけど、pagination_class指定のクラスのget_paginated_responseを実行する)
            return self.get_paginated_response(response_serializer.data)

        # ページネーションされなかった場合（たとえば設定ミス時用）
        response_serializer = BlogResponseSerializer(queryset, many=True)
        return Response(response_serializer.data)
    
    def retrieve(self, request, pk=None):
        # 詳細取得のAPIの方では、クエリパラメータを受ける可能性がほぼないのでリクエスト用シリアライザがいらない(例えば言語で出し分けたりする場合はありえるかもだが。)
        # クエリも使わない理由についても同様(例えば、そのブログが公開の状態なのであれば取得するとか)
        try:
            blog = Blog.objects.get(pk=pk)
        except Blog.DoesNotExist:
            raise NotFound(detail="Blog not found")

        serializer = BlogResponseSerializer(blog)
        return Response(serializer.data)
    # def create(self, request, *args, **kwargs):
    # # このメソッドは意図的に500エラーを発生させるために使っていました。今後は使わない
    #     raise Exception("意図的な500 Internal Server Error")

    def create(self, request, *args, **kwargs):
        # TODO: 今のところブログ作成機能はview、serializer含めかなり記述量がすくない。
        # しかし、①ログインしたユーザーのみ作成許可や、②同じタイトルをつけることができないようにする場合
        # ③タグ機能など、他モデルとの連携でトランザクションデータにしないといけない場合
        # ④作成のため使うシリアライザにhelp_textやlabel、exampleをつける場合
        # などを考慮する場合があるかも
        serializer = BlogCreateRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        blog = Blog.objects.create(**serializer.validated_data)
        response_serializer = BlogResponseSerializer(blog)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
# ---viewsets.GenericViewを継承したクラスの中で、「その変数に値を入れることに意味が出てくる」もの----
# https://www.cdrf.co/
# https://www.cdrf.co/3.14/rest_framework.viewsets/GenericViewSet.html
# https://www.django-rest-framework.org/api-guide/views/
# https://www.django-rest-framework.org/api-guide/generic-views/
# https://note.crohaco.net/2018/django-rest-framework-view/
# pagination_class	-> ページネーションクラスを指定
# -> self.paginate_queryset()でページネーションスライス処理、self.get_paginated_response()でページつきのレスポンスを作成
# -> (この変数を使わないならsettings.py の設定が使われる)

# serializer_class	-> レスポンス・リクエスト用シリアライザを指定
# ->self.get_serializer()とするとこの変数のクラスのget_serializerが使われて、シリアライザが決定
# -> (この変数を使わないと「なし=シリアライザを使わない」（手動指定が基本）)

# filter_backends	-> フィルタリングロジックを自動適用
# ->(この変数を使わないならsettings.py の設定が使われる)

# permission_classes -> アクセス制御（認可）
# -> self.get_permissions()でアクセス制御方法を取得する
# ->(この変数を使わないと「AllowAny」（誰でもOK）)

# authentication_classes -> 認証方法（JWT, セッション等）
# -> self.get_authenticators()で認証方式の選択
# ->(この変数を使わないと「セッション or Basic」)

# throttle_classes -> レート制限を指定
# ->(この変数を使わないなら、レート制限は指定なし)

# queryset -> 対象モデルのクエリセット
# -> self.get_queryset()でquerysetに入れたクラスのget_querysetメソッドを使い、データを取得する
# ->(この変数を使わないならなし（または get_queryset() のオーバーライドしても代用できる））

# lookup_field -> retrieve() などの検索キー（通常は pk）
# ->(この変数を使わないと"pk"をいれたことになる)

# renderer_classes -> レンダラー（JSON, HTML, Browsable APIなど）
# -> self.get_renderer_context()でレスポンスの形式(JSONかどうかなど)の決定をする
# ->(この変数を使わない場合settingsの REST_FRAMEWORK["DEFAULT_RENDERER_CLASSES"]に依存する)

# viewsets.GenericAPIViewを継承したクラスベースビューは、CRUDの内1つだけ実装した場合(ヘルスチェック用とか)の場合につかう。
# viewsets.ModelViewSetを継承したクラスベースビューは、CRUDの全てを実装した場合につかう。

# ---viewsets.GenericViewを継承したクラスの中で、「その変数に値を入れることに意味が出てくる」もの----


    