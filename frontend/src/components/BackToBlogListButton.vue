<!-- これは共通コンポーネントの遷移ボタンです。 -->
<template>
    <button
      @click="goBack"
      class="px-4 py-2 rounded bg-gray-200 hover:bg-gray-300"
      data-testid="back-to-blog-list-btn"
    >
      戻る
    </button>
</template>
  
<script setup lang="ts">
    // この共通コンポーネントでは、現在「戻る」ボタンとしての機能にすることを想定しています。
    // なので、上のtemplateのbuttonが押されると、goBack定数の無名関数が実行され、vue-routerを使用して、ブログ一覧ページに遷移するようにしています。 
    import { useRouter } from 'vue-router'

    const router = useRouter()
    const goBack = () => {
        router.push('/blogs')
    }
</script>
  