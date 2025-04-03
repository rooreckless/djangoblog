import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import router from './router' // このファイルからみてrouterディレクトリ内のtsファイルなどから、変数routerをimport

const app = createApp(App)   // vueアプリを作成し変数に格納
app.use(router)              // アプリとしてvue-routerを使用する設定
app.mount('#app')