from django.contrib import admin

# Register your models here.
from api.models.blogs import Blog
# admin画面でログイン後にBlogモデルが表示されるようにするにはこれ↑&↓が必要
@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'created', 'modified')  # ← 管理一覧画面で表示する列
    readonly_fields = ('created', 'modified')  # ← 編集画面で編集不可にする
