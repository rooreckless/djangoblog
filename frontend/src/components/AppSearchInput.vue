<template>
    <div class="flex items-center gap-2">
        <!-- テキスト入力欄。入力された値はv-modelでこのコンポーネントのscrtiptで定義のref変数keywordと同期。-->
         <!--Enterキー押下時にsubmitSearch関数を実行 -->
        <input
            type="text"
            v-model="keyword"
            @keydown.enter="submitSearch"
            class="border px-3 py-2 rounded w-full"
            :placeholder="placeholder"
        />
        <!-- 検索ボタン。クリック時にsubmitSearch関数を実行 -->
        <button
            @click="submitSearch"
            class="px-4 py-2 rounded bg-sky-400 text-white hover:bg-sky-500"
        >
        検索
        </button>
    </div>
</template>
  
<script setup lang="ts">
import { ref, defineEmits, defineProps } from 'vue'
// 親コンポーネントで受け取るpropsとしては、入力欄のplaceholder
const props = defineProps<{
    placeholder?: string
}>()


// emitイベントの定義。
// このコンポーネントは "search" イベントを親に向けて発行する。引数は文字列（検索語）
const emit = defineEmits<{
    (e: 'search', value: string): void
}>()

// 入力フォームにバインドする状態(keyword)
const keyword = ref('') // 初期状態は空文字列

const submitSearch = () => {
    emit('search', keyword.value);  // 現在の入力値と"search"イベントを親コンポーネントへ渡す
    // 親コンポーネントにて、このコンポーネントを使う際は、@search="実行したい関数"のようにしている
    //  = ここが実行されたら、searchイベントが親コンポーネントに飛び、その「実行したい関数」が実行される
    //　そのsearchイベントによって実行される関数に引数で渡るのがkeyword.valueです。

}
</script>
  