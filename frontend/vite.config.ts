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

//-------------

// import { defineConfig } from 'vite'
// import vue from '@vitejs/plugin-vue'
// import tailwindcss from '@tailwindcss/vite'
// import path from 'path'
// export default defineConfig({
//   base: "/",  // ルート配信
//   build: {
//     outDir: "dist",
//   },
//   plugins: [
//     vue(),
//     tailwindcss(),
//   ],
//   //importする時のパスの入力に、@で示すルートディレクトリの位置を指定
//   resolve: {
//     alias: {
//       '@': path.resolve(__dirname, './src') // @でsrcディレクトリを指すように設定
//     }
//   },
//   server: {
//     host: "0.0.0.0",  // コンテナ外からアクセス可能にする
//     port: 5173,       // デフォルトポート
//     watch: {
//       usePolling: true, // WSL2 や Docker でホットリロードを確実に機能させる
//     },
//     allowedHosts: ['frontend'], // ← Playwright などからのアクセス用 page.content()をplaywrightのテストケースにいれたらエラーだったので。
//   },
//   test: {
//     environment: 'jsdom',     // ← 仮想ブラウザ環境を指定
//     globals: true,             // it/test/expect をグローバルに使えるように
//     include: ['tests/**/*.test.ts'], // 任意：テスト対象ファイルのパターン
//   },
// })


//----------------
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import tailwindcss from '@tailwindcss/vite'
import { fileURLToPath, URL } from 'node:url'

export default defineConfig({
  base: "/",
  build: {
    outDir: "dist",
  },
  plugins: [
    vue(),
    tailwindcss(),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
    }
  },
  server: {
    host: "0.0.0.0",
    port: 5173,
    watch: {
      usePolling: true,
    },
    allowedHosts: ['frontend','localhost', 'host.docker.internal'],
  }
})
