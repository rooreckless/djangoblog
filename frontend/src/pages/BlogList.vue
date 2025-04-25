<template>
  <div class="container mx-auto px-4 py-8">
    <h1 data-testid="bloglist-section-title" class="text-2xl font-bold mb-4">ブログ一覧</h1>
    <!-- ▶ ドロップダウン：ページサイズ選択 -->
    <div class="mb-4 flex items-center space-x-2 justify-around">
      <div>
      <label for="page-size" class="text-sm">1ページに表示する件数：</label>
      <select
        id="page-size"
        v-model="pageSize"
        class="border rounded px-2 py-1"
      >
        <option :value="5">5件</option>
        <option :value="10">10件</option>
        <option :value="20">20件</option>
        <option :value="50">50件</option>
      </select>
      </div>
      <!-- ブログ作成画面への遷移ボタン -->
      <AppTrasitionPageButton to="/blogs/create" data-testid="bloglist-transition-blogcreate-btn">
          ブログ作成画面へ
      </AppTrasitionPageButton>
    </div>

    <!-- ▶ ブログ一覧 -->
    <div class="space-y-4" data-testid="bloglist-blogs-container">
      <div
        v-for="blog in blogs"
        :key="blog.id"
        data-testid="bloglist-blog-item"
        class="p-4 rounded-xl shadow bg-white border"
      >
      <router-link :to="`/blogs/${blog.id}`" :data-testid="`bloglist-blog-title-link-${blog.id}`">
        <h2 class="text-lg font-semibold" :data-testid='`bloglist-blog-title-${blog.id}`'>
          {{ blog.title }}
        </h2>
      </router-link>

        <p class="text-gray-500 text-sm">
          投稿日: {{ moment(blog.created).format("YYYY年MM月DD日 HH:mm:ss") }}
        </p>
        <p class="mt-2 text-gray-700  line-clamp-2">{{ blog.contents_text }}</p>
      </div>
    </div>

    <!-- ページネーション -->
    <div class="mt-6 flex justify-center items-center space-x-4">
      <button
        class="px-4 py-2 rounded bg-gray-200 hover:bg-gray-300"
        @click="currentPage--"
        :disabled="currentPage <= 1"
        data-testid="bloglist-previouspage-btn"
      >
        前へ
      </button>

      <span>{{ currentPage }} / {{ totalPages }}</span>

      <button
        class="px-4 py-2 rounded bg-gray-200 hover:bg-gray-300"
        @click="currentPage++"
        :disabled="currentPage >= totalPages"
        data-testid="bloglist-nextpage-btn"
      >
        次へ
      </button>
    </div>
  </div>
</template>

  
<script setup lang="ts">
  import { ref, onMounted, watch } from "vue";
  import moment from "moment"
  // 共通コンポーネントである「遷移ボタン」をインポート
  import AppTrasitionPageButton from '@/components/AppTrasitionPageButton.vue'
 
  const baseURL = import.meta.env.VITE_API_BASE_URL;
  const blogs = ref([]);
  const currentPage = ref(1);
  const pageSize = ref(10);
  const totalPages = ref(1);

  
  const getBlogLists = async ()=>{
    try {
      const response = await fetch(`${baseURL}/api/v1/blogs/?page=${currentPage.value}&size=${pageSize.value}`);
      const results = await response.json();
      blogs.value = results["results"];
      totalPages.value = Math.ceil(results["num_of_items"] /pageSize.value);
    } catch (error) {
      console.error("Error fetching blogs:", error);
    }
  };


  
  const init = async ()=>{
    
    await getBlogLists();
  };
    onMounted(() => {
        init();

  });
    
  watch([currentPage, pageSize],async () => {
    totalPages.value = Math.ceil(blogs.value.length/pageSize.value);
    await getBlogLists();
  });

</script>
  