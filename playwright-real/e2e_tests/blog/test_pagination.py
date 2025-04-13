from playwright.sync_api import Page, expect
import time

# 一番カンタンなe2eテストケース(あらかじめブログが13件登録されている状態で実施しないとエラーになる)
def test_pagination_works(page: Page):
    page.goto("http://frontend:5173/blogs/")

    # ✅ 最初のページで bloglist-blog-item が10件だけあることを確認
    expect(page.get_by_test_id("bloglist-blog-item")).to_have_count(10)

    # ✅ 次ページに進む（data-testid="next-page" を想定）
    page.get_by_test_id("bloglist-nextpage-btn").click()

    # ✅ 次ページにも bloglist-blog-item が表示される（残りの件数によって変化）
    expect(page.get_by_test_id("bloglist-blog-item")).to_have_count(3)  # ← 13件の2ページ目でデフォルト設定なら3件になるはず
