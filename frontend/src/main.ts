import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import router from './router' // このファイルからみてrouterディレクトリ内のtsファイルなどから、変数routerをimport

// 共通コンポーネント
import AppTrasitionPageButton from '@/components/AppTrasitionPageButton.vue'
import AppSearchInput from '@/components/AppSearchInput.vue'

const app = createApp(App)   // vueアプリを作成し変数に格納

// 共通コンポーネントを、その個数分appに登録 = 各vueファイルで共通コンポーネントをimportせずに使えるようにする
app.component('AppTrasitionPageButton', AppTrasitionPageButton) 
app.component('AppSearchInput', AppSearchInput) 

app.use(router)              // アプリとしてvue-routerを使用する設定
app.mount('#app')