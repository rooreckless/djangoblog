import { mount } from '@vue/test-utils'
import BackToBlogListButton from '@/components/BackToBlogListButton.vue'
import { describe, test, expect, vi } from 'vitest'
import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(),
  routes: [],
})

describe('BackToBlogListButton', () => {
  test('クリックすると /blogs に遷移する', async () => {
    router.push = vi.fn()

    const wrapper = mount(BackToBlogListButton, {
      global: {
        plugins: [router],
      },
    })

    await wrapper.get('[data-testid="back-to-blog-list-btn"]').trigger('click')
    expect(router.push).toHaveBeenCalledWith('/blogs')
  })
})