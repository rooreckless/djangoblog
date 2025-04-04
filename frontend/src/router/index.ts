// src/router/index.ts
import { createRouter, createWebHistory } from 'vue-router'
// ルーティングを記載する部分
const routes = [
  {
    path: '/blogs',
    name: 'BlogList',
    component: () => import('@/pages/BlogList.vue'), // 後ほど作成
  },
  {
    path: '/blogs/:id',
    name: 'BlogDetail',
    component: () => import('@/pages/BlogDetail.vue'), // 後ほど作成
  },
]
// main.tsでよみこむrouter(はcreateRouterオブジェクト)
const router = createRouter({
  history: createWebHistory(),
  routes,
})
// routerは外部tsファイル(main.ts)で読み込めるようにする
export default router
