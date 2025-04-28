// これは、Vue.jsのコンポーネントのユニットテストを行うためのコードです。
import { mount } from '@vue/test-utils'
// テスト対象のコンポーネントをインポート
import { describe, test, expect, vi } from 'vitest'
import AppTrasitionPageButton from '@/components/AppTrasitionPageButton.vue'
import { createRouter, createWebHistory } from 'vue-router' // router-link を正しく動作させるために router を作成

describe('AppTrasitionPageButton', () => {
  test('クリックすると router.push が呼ばれる', async () => {
    // Vitest のモック関数を作成
    const mockPush = vi.fn()

    const router = createRouter({
        history: createWebHistory(),  // HTML5の履歴モード
        routes: [
          { path: '/', component: { template: '<div>Home</div>' } }
        ] // テストでは実際のルートは必要ない（ルーティング自体はしないので）
    })

    // 実際の router.push を、上で作ったモック関数に差し替える
    router.push = mockPush

    const wrapper = mount(AppTrasitionPageButton, {
      props: {
        to: '/dashboard',   // ボタンクリック時に遷移してほしいパス(このテスト用)
      },
      slots: {
        default: '戻るよ',  // スロットに渡す内容=ボタンの表示テキスト（デフォルトスロット）propsで渡すのではない
      },
      attrs: {
        'data-testid': 'test-back-btn', // テストでボタンを識別するための属性(props ではなく attrs で渡す)
      },
      global: {
        plugins: [router],  // Vue Router をプラグインとして登録（useRouter を動作させるため）
      },
    })
    // ボタン要素を取得（data-testidで識別）
    const target_btn = wrapper.get('[data-testid="test-back-btn"]')
    // ボタンの表示テキストが props で渡したものと一致するか確認
    expect(target_btn.text()).toBe('戻るよ')
    // ボタンをクリック
    target_btn.trigger('click') 
    // モック関数 mockPush（= router.push）が '/dashboard' を引数に呼ばれたことを検証
    expect(mockPush).toHaveBeenCalledWith('/dashboard')
  })
})
