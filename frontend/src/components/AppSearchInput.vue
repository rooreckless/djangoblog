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
            :data-testid="`${props.dataTestid}-input`"
        />
        <!-- 検索ボタン。クリック時にsubmitSearch関数を実行 -->
        <button
            @click="submitSearch"
            class="px-4 py-2 rounded bg-sky-400 text-white hover:bg-sky-500"
            :data-testid="`${props.dataTestid}-btn`"
        >
        検索
        </button>
    </div>
</template>
  
<script setup lang="ts">
// defineEmits, defineProps,withDefaultsはvueからimportしなくてもいいようになっている
import { ref } from 'vue'
// 親コンポーネントで受け取るpropsとしては、入力欄のplaceholderとdateTestid

const props = withDefaults(defineProps<{
    placeholder?: string,
    dataTestid: string  // ← シングルクォートで囲って定義できる（ハイフンを含む名前だから）
}>(), {
    // 個々に記述しているのはデフォルト値(変数名にシングルクォートを使う場合についても一緒)
    placeholder: '検索',
    dataTestid: 'search-bar'
})

// emitは、Vueのコンポーネントから親コンポーネントにイベントを発火するためのもの
// このコンポーネントは "search" イベントを親に向けて発行する。発行した際、親に渡す値の型はstring型=検索文字列
const emit = defineEmits<{
    (e: 'search', value: string): void
}>()
// 上記はjsとして記述するなら、defineEmits()だけになるが、defineEmits自体がジェネリクス関数として定義されている。
// なので、<>の部分は「emitにいれる引数の型」を定義することになる。で、指定したものは{} = オブジェクトだがそれは「関数型(シグネチャ型)」
// 「戻り値はなし(void)で、"search"というイベントが発生した時、親コンポーネントへ渡す値はstring型に決める」というもの
// 「引数の型だけ決めておいて、実際の引数がない」のはdefineEmitsの仕様。あくまで、「イベント名を指定し、それが発火した時に渡る値の型だけ決めておきたい」だけだから。
// 下のsubmitSearchの中身がそのようになっている。
// そして、親コンポーネントでは@search=handleSearchと書いてあるので、「親コンポーネントのhandleSearchメソッドでは、「子コンポーネントでsearchイベント発生時用に準備していた値(keyword.value)」が引数としてわたってきて使えるようになる。」


// 入力フォームにバインド(v-model)する状態(keyword)
const keyword = ref('') // 初期状態は空文字列

const submitSearch = () => {
    emit('search', keyword.value);  // 現在入力されている値を "search" イベントとして親に送信する
    // 親コンポーネントでは、このコンポーネントに @search="handleSearch" のように登録しておくことで、
    // この "search" イベントが発火されたとき、親側の handleSearch 関数が実行される。
    // handleSearch 関数の引数には、ここで emit した keyword.value の値（string型）が渡される

}
</script>


<!-- https://typescriptbook.jp/reference/values-types-variables/literal-types -->
<!-- https://typescriptbook.jp/reference/generics -->
<!-- https://typescriptbook.jp/reference/generics/type-variables -->
<!-- https://typescriptbook.jp/reference/functions/function-type-declaration#%E3%83%A1%E3%82%BD%E3%83%83%E3%83%89%E6%A7%8B%E6%96%87%E3%81%AB%E3%82%88%E3%82%8B%E9%96%A2%E6%95%B0%E3%81%AE%E5%9E%8B%E5%AE%A3%E8%A8%80 -->