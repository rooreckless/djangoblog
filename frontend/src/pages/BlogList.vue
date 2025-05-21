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
      <!-- 共通コンポーネントのブログ検索欄 searchイベント発生時にはhandleSearchを実行する-->
      <AppSearchInput placeholder="検索" @search="handleSearch" dataTestid="bloglist-search"/>
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
  
  // interface
  interface Blog {
    id: number
    title: string
    contents_text: string
    created: string  // 日付はISO文字列として扱う場合は string
  }
  interface BlogListResponse {
    results: Blog[]
    num_of_items: number
  }

  const baseURL = import.meta.env.VITE_API_HOST_ADDRESS;
  // const blogs = ref([]);
  const blogs = ref<Blog[]>([]);
  // const searchword = ref("");
  // const currentPage = ref(1);
  // const pageSize = ref(10);
  // const totalPages = ref(1);

  const searchword = ref<string>('')
  const totalPages = ref<number>(1)
  const currentPage = ref<number>(1)
  const pageSize = ref<number>(10)


  // methods  
  const getBlogLists = async ()=>{
    try {
      const response = await fetch(`${baseURL}/api/v1/blogs/?page=${currentPage.value}&size=${pageSize.value}`);
      console.log("-|-baseURL=",baseURL)
      console.log("---response=",response)
      // console.log("---await response.json()=",await response.json())
      // const responseBody = await response.json();
      const responseBody: BlogListResponse = await response.json()
      blogs.value = responseBody["results"];
      totalPages.value = Math.ceil(responseBody["num_of_items"] /pageSize.value);
    } catch (error) {
      console.error("Error fetching blogs:", error);
    }
  };
  // 共通コンポーネント
  // emitで発火したイベントによって実行する関数
  // 引数valueはemit になっているもう一つの引数
  const handleSearch = async (value: string) => {
    // console.log("検索キーワード:", value);
    searchword.value = value;
    // 検索キーワードを使ってブログリストを取得するAPIを呼び出す
    const response = await fetch(`${baseURL}/api/v1/blogs/?title=${value}&page=${currentPage.value}&size=${pageSize.value}`);
    const responseBody = await response.json();
    blogs.value = responseBody["results"];
    totalPages.value = Math.ceil(responseBody["num_of_items"]/pageSize.value);
    return;
  }

  // init
  const init = async ()=>{
    
    await getBlogLists();
  };

  // onMounted
  onMounted(() => {
        init();

  });
  // watch
  watch([currentPage, pageSize],async () => {
    totalPages.value = Math.ceil(blogs.value.length/pageSize.value);
    await handleSearch(searchword.value);
  });

</script>
  