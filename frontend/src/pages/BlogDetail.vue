<!-- src/pages/BlogDetail.vue -->
<template>
  <div class="p-4">
    <h1 class="text-2xl font-bold mb-4">ブログ詳細</h1>
    <div v-if="blog">
      <h2 class="text-xl font-semibold">{{ blog.title }}</h2>
      <p class="text-gray-600 text-sm mb-2">投稿日: {{ blog.created }}</p>
      <p>{{ blog.contents_text }}</p>
    </div>
    <div v-else>
      ロード中...
    </div>
  </div>

  <!-- 削除ボタンと戻るボタン -->
  <div class="mt-6 mx-4 flex justify-between items-center space-x-4">
    <button
      class="px-4 py-2 rounded bg-gray-200 hover:bg-gray-300"
      @click="backBlogListPage"
    >
      戻る
    </button>

    <button
      class="px-4 py-2 rounded bg-gray-200 hover:bg-gray-300"
      @click="deleteBlogDetail"
    >
      削除
    </button>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import { useRoute,useRouter } from "vue-router";

const blog = ref(null);
const route = useRoute();
const router = useRouter()

onMounted(async () => {
  const id = route.params.id;
  const response = await fetch(`http://localhost:8000/api/v1/blogs/${id}/`);
  blog.value = await response.json();
});

const backBlogListPage = ()=>{
  console.log("--戻るボタン--")
  router.push('/blogs')  // 一覧画面に戻る
};

const deleteBlogDetail = ()=>{
  console.log("--削除ボタン--")
};
</script>
