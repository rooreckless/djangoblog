<template>
  <div class="container mx-auto px-4 py-8">
    <h1 data-testid="section-title" class="text-2xl font-bold mb-4">ブログ一覧</h1>
    <!-- ▶ ドロップダウン：ページサイズ選択 -->
    <div class="mb-4 flex items-center space-x-2">
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

    <!-- ▶ ブログ一覧 -->
    <div class="space-y-4" data-testid="blogs_container">
      <div
        v-for="blog in blogs"
        :key="blog.id"
        data-testid="blog-item"
        class="p-4 rounded-xl shadow bg-white border"
      >
      <router-link :to="`/blogs/${blog.id}`" data-testid="blog-title-link">
        <h2 class="text-lg font-semibold">
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
      >
        前へ
      </button>

      <span>{{ currentPage }} / {{ totalPages }}</span>

      <button
        class="px-4 py-2 rounded bg-gray-200 hover:bg-gray-300"
        @click="currentPage++"
        :disabled="currentPage >= totalPages"
      >
        次へ
      </button>
    </div>
  </div>
</template>

  
<script setup lang="ts">
  import { ref, onMounted, watch } from "vue";
  import moment from "moment"

  const baseURL = import.meta.env.VITE_API_BASE_URL;
  const blogs = ref([]);
  const currentPage = ref(1);
  const pageSize = ref(10);
  const totalPages = ref(1);

  
  const getBlogLists = async ()=>{
    // // const response = await fetch("http://localhost:8000/api/v1/blogs/");
    // const response = await fetch(`http://localhost:8000/api/v1/blogs/?page=${currentPage.value}&size=${pageSize.value}`);
    // // const response = await fetch(`http://backend:8000/api/v1/blogs/?page=${currentPage.value}&size=${pageSize.value}`);
    // let results=await response.json();
    // blogs.value = results["results"];
    // totalPages.value = results["num_of_pages"];
    try {
      // const response = await fetch(`http://backend:8000/api/v1/blogs/?page=${currentPage.value}&size=${pageSize.value}`);
      // const response = await fetch(`http://localhost:8000/api/v1/blogs/?page=${currentPage.value}&size=${pageSize.value}`);
      const response = await fetch(`${baseURL}/api/v1/blogs/?page=${currentPage.value}&size=${pageSize.value}`);
      const results = await response.json();
      console.log("Fetched results:", results);  // ← 追加
      blogs.value = results["results"];
    } catch (error) {
      console.error("Error fetching blogs:", error);  // ← 追加
    }
  };

  
  const init = async ()=>{
    await getBlogLists();
  };
    onMounted(() => {
        init();

  });
    
  watch([currentPage, pageSize], () => {
    getBlogLists();
  });

</script>
  