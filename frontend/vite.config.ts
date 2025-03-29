// import { defineConfig } from 'vite'
// import vue from '@vitejs/plugin-vue'
// import tailwindcss from '@tailwindcss/vite'
// export default defineConfig({
//   plugins: [
//     vue(),
//     tailwindcss(),
//   ],
//   server: {
//     host: "0.0.0.0",  // コンテナ外からアクセス可能にする
//     port: 5173,       // デフォルトポート
//     watch: {
//       usePolling: true, // WSL2 や Docker でホットリロードを確実に機能させる
//     },
//   },
// })

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import tailwindcss from '@tailwindcss/vite'
export default defineConfig({
  base: "/",  // ルート配信
  build: {
    outDir: "dist",
  },
  plugins: [
    vue(),
    tailwindcss(),
  ],
  server: {
    host: "0.0.0.0",  // コンテナ外からアクセス可能にする
    port: 5173,       // デフォルトポート
    watch: {
      usePolling: true, // WSL2 や Docker でホットリロードを確実に機能させる
    },
  },
})