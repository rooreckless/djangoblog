// このファイルがvitestのテストファイルです。

// Vitest の基本的なテスト構文を提供（Jest 互換）。
import { describe, test, expect } from 'vitest'
// Vueコンポーネントを実際の DOM としてマウントするための関数。
import { mount } from '@vue/test-utils'
// テスト対象のブログ作成画面の Vue コンポーネント。
import BlogCreate from '@/pages/BlogCreate.vue'
import { createRouter, createWebHistory } from 'vue-router'
// vitestでは、main.tsが読み込まれないので共通コンポーネントをインポート
import AppTrasitionPageButton from '@/components/AppTrasitionPageButton.vue'
// 以下を用意して、BlogCreate.vueをマウントする時にpluginとして渡さないと、警告がでる
const router = createRouter({
    history: createWebHistory(),  // HTML5の履歴モード
    routes: [
      { path: '/', component: { template: '<div>Home</div>' } }
    ] // テストでは実際のルートは必要ない（ルーティング自体はしないので）
})

// 以下describeが、その中野testをまとめるためのもの。
describe('BlogCreate.vue - 作成ボタンの状態制御', () => {
    // testは、テストケースを定義するための関数。
    test('フォームが有効なとき、作成ボタンは有効化されスタイルが変わる', async () => {
        //BlogCreate.vue をマウント（仮想DOMに展開）し、wrapper オブジェクトを取得。
        const wrapper = mount(BlogCreate, {
            global: {
                plugins: [router],
                components: {
                    AppTrasitionPageButton,
                },
            },
          })
        // ボタン要素を取得　data-testid を使って「作成」ボタン要素を、全体DOMのwrapperから取得。
        const submitBtn = wrapper.get('[data-testid="blogcreate-submit-btn"]')
        // フィールドに入力をしていない状態だと、作成ボタンは灰色で押せないはず
        // 押せないことをtailwindcssのクラスで、確認(色 + 押せないこと)
        expect(submitBtn.classes()).toContain('bg-gray-100')
        expect(submitBtn.classes()).toContain('cursor-not-allowed')
        // 作成ボタンにはdisabled属性がついているはず
        expect(submitBtn.attributes('disabled')).toBeDefined()
        // 作成ボタンにはdisabled属性自体に値が入っていないはず(なくてもdisabledになるし)
        expect(submitBtn.attributes('disabled')).toBe("")
        // 必須フィールドに入力（data-testidで）
        const titleInput = wrapper.get('[data-testid="blogcreate-input-title"]')
        const contentTextarea = wrapper.get('[data-testid="blogcreate-textarea-contents-text"]')
        // フィールドに値が入ったかを確認
        await titleInput.setValue('テストタイトル')
        await contentTextarea.setValue('テスト本文')


        // ボタンが有効かどうか確認
        expect(submitBtn.attributes('disabled')).toBeUndefined()

        // スタイル確認（Tailwindなどでclassが変わる場合）
        expect(submitBtn.classes()).toContain('hover:bg-gray-300') // hover時の色を確認
        expect(submitBtn.classes()).toContain('bg-sky-400')         // 押せる状態のボタンであるかを確認
        expect(submitBtn.classes()).not.toContain('bg-gray-100')    // 無効時ではないことを確認
        expect(submitBtn.classes()).not.toContain('cursor-not-allowed')
    })
})

// こういったフロントのユニットテストとして作成すべき内容としては
// 表示切替やローディングなどの「要素の状態を確認するテスト」である
// 仮に「他の画面とも共通しやすい部分」だったならば、コンポーネントとしてわけてしまい、「わけたコンポーネント用のテスト」としていい


// --ユニットテストが必要になるパターンとは？--

// ユースケース	理由
// ✅ 複雑なフォーム入力処理	例: 日付選択 → バリデーション → 送信データの整形など
// ✅ 条件分岐の多いUIロジック	例: ロールによって表示ボタンが変わる・エラーハンドリング分岐
// ✅ コンポーネントが状態に応じて切り替わる	例: ローディング→成功→失敗のステートを持つ
// ✅ PiniaやVuexのストアと連携している	コンポーネントがグローバルな状態を利用してUIを切り替えている
// ✅ ユーザーの入力やイベントに応じて関数が実行される	click, hover, 入力などによってロジックが走る

// なので、ユニットテストが真価を発揮するのは「入力処理 + ロジック」のあるコンポーネント
// タイトル未入力なら「保存ボタン」が押せない	wrapper.find('button').element.disabled === true
// 入力された本文がそのままデータとして渡される	expect(emitted().submit[0]).toEqual([expectedPayload])
// エラーメッセージが表示される	expect(wrapper.text()).toContain('タイトルは必須です')



// E2E テストが優れている理由（現状の構成において）
// 項目	内容
// ✅ 全体のつながりを確認できる	Vue → API（Django）→ DB という一連の流れが動作するかをテストできる
// ✅ fetch など非同期も自然に検証できる	実際に画面を操作して確認するので、実用に近いテストができる
// ✅ ユーザー視点のテスト	「ページを開いたらブログが表示される」というようなUXに近い確認ができる
// ✅ 現状のVueに「複雑なロジックがない」	単純にAPIを叩いて描画するだけなら、ユニットテストのメリットが薄い


// 実行コマンドは docker compose -f local.yml run --rm frontend npm run test:unitだと対話式= watchモード
// docker compose -f local.yml run --rm frontend npx vitest でも同様に対話式 = watchモード

// docker compose -f local.yml run --rm frontend npx vitest run tests だと対話式ではない

// ファイルを指定したいなら　docker compose -f local.yml run --rm frontend npx vitest run tests/unit/BlogCreate.test.ts
// ケースを絞りたいなら　docker compose -f local.yml run --rm frontend npx vitest run -t "フォームが有効なとき、作成ボタンは有効化されスタイルが変わる"
// -t オプションは、上記ファイルのtestのタイトル、またはdescribeのタイトルを指定
// testのタイトルは、複数describeが記述できるとしてもユニークにしておいた方がよい