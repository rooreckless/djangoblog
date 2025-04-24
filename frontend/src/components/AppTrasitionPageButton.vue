<!-- これは共通コンポーネントの遷移ボタンです。 -->
<template>
  <button
    type="button"
    @click="transitionPageTo"
    :class="[
      'px-4 py-2 rounded',
      'hover:bg-gray-300',
      'bg-gray-200'
    ]"
    v-bind="$attrs"
  >
    {{ text }}
  </button>
</template>
<script setup lang="ts">
// この共通コンポーネントでは、「どこかへ遷移」するためのボタンとしての機能にすることを想定しています。
// なので、上のtemplateのbuttonが押されると、goBack定数の無名関数が実行され、vue-routerを使用して、ブログ一覧ページに遷移するようにしています。 
// transitionPageToの関数ではprops.toが指定されていればそのURLに遷移し、指定されていなければ'/blogs'に遷移するようにしています。
// props.toの値の指定の仕方は、<AppTransitionPageButton to="/blogs" text="ブログ一覧へ戻る" date-testid="some-datetest-id"/>のようにします。
import { useRouter } from 'vue-router'
import { defineProps,withDefaults } from 'vue'

// 明示的に受け取る props（その他は $attrs）
// 特にdatatestidはpropsで渡すことができないのでattrsで受け取るようにしています。
const props = withDefaults(defineProps<{
  to?: string
  text?: string
  
}>(), {
  to: '/blogs',
  text: '戻る',
})

const router = useRouter()

const transitionPageTo = () => {
  router.push(props.to ?? '/blogs')
}

</script>