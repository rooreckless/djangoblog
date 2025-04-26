import { mount } from '@vue/test-utils'
import { describe, test, expect, vi } from 'vitest'
import AppSearchInput from '@/components/AppSearchInput.vue' // ←ファイルパスは適宜変更してください

describe('AppSearchInput.vue', () => {
  test('初期状態では入力欄は空文字', () => {
    const wrapper = mount(AppSearchInput)

    const input = wrapper.get('input')
    expect((input.element as HTMLInputElement).value).toBe('')
  })

  test('propsでplaceholderが反映される', () => {
    const wrapper = mount(AppSearchInput, {
      props: {
        placeholder: 'キーワードを入力してください',
      },
    })

    const input = wrapper.get('input')
    expect(input.attributes('placeholder')).toBe('キーワードを入力してください')
  })

  test('入力するとv-modelが反映される', async () => {
    const wrapper = mount(AppSearchInput)

    const input = wrapper.get('input')
    await input.setValue('Vue3テスト')

    // 入力した値が input に反映されていることを確認
    expect((input.element as HTMLInputElement).value).toBe('Vue3テスト')
  })

  test('ボタンをクリックするとsearchイベントがemitされる', async () => {
    const wrapper = mount(AppSearchInput)

    const input = wrapper.get('input')
    await input.setValue('クリックで検索')

    const button = wrapper.get('button')
    await button.trigger('click')

    // emitが発火しているか、payloadが正しいか
    expect(wrapper.emitted('search')).toBeTruthy()
    expect(wrapper.emitted('search')![0]).toEqual(['クリックで検索'])
  })

  test('Enterキー押下でもsearchイベントがemitされる', async () => {
    const wrapper = mount(AppSearchInput)

    const input = wrapper.get('input')
    await input.setValue('エンターで検索')

    // Enterキーイベントをシミュレート
    await input.trigger('keydown.enter')

    expect(wrapper.emitted('search')).toBeTruthy()
    expect(wrapper.emitted('search')![0]).toEqual(['エンターで検索'])
  })
})
