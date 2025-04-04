// // frontend/tests/unit/first.test.ts
// import { describe, it, expect, vi, beforeEach } from 'vitest'
// import { mount } from '@vue/test-utils'
// import BlogList from '@/pages/BlogList.vue'

// // テスト用のモックデータ
// const mockBlogs = {
//   results: [
//     { id: 1, title: "タイトル_1", contents_text: "コンテンツ_1", created: "2024-04-01T00:00:00Z" },
//     { id: 2, title: "タイトル_2", contents_text: "コンテンツ_2", created: "2024-04-02T00:00:00Z" }
//   ],
//   current_page: 1,
//   num_of_items: 2,
//   num_of_pages: 1,
//   num_of_items_per_page: 10
// }

// describe('BlogList.vue', () => {
//   beforeEach(() => {
//     // fetch をモック
//     global.fetch = vi.fn(() =>
//       Promise.resolve({
//         json: () => Promise.resolve(mockBlogs),
//       } as Response)
//     )
//   })

//   it('初期表示でブログが2件描画される', async () => {
//     const wrapper = mount(BlogList)
//     // 表示を待つ（非同期fetch → DOM更新）
//     await new Promise(resolve => setTimeout(resolve, 0))
//     expect(wrapper.text()).toContain("タイトル_1")
//     expect(wrapper.text()).toContain("タイトル_2")
//   })
// })


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
