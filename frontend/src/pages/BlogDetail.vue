<!-- src/pages/BlogDetail.vue -->
<template>
  <div class="container mx-auto px-4 py-8">
    <h1 class="text-2xl font-bold mb-4">ブログ詳細</h1>
    <div v-if="blog">
      <h2 class="mb-2 p-4 rounded-xl shadow bg-white bordertext-xl font-semibold w-full" data-testid="blogretrive-blog-title">{{ blog.title }}</h2>
      <p class="text-gray-600 text-sm mb-2">投稿日: {{ blog.created }}</p>
      <p  data-testid="blogretrive-blog-contents-text" class ="w-full p-4 rounded-xl">{{ blog.contents_text }}</p>
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

// interface
interface Blog {
  id: number
  title: string
  contents_text: string
  created: string  // 日付はISO文字列として扱う場合は string
}
const blog = ref<Blog>();
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
