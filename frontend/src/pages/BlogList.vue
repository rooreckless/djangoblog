<!-- src/pages/BlogList.vue -->
<template>
    <div class="p-4">
      <h1 class="text-2xl font-bold mb-4">ブログ一覧</h1>
      
      <ul>
        <li
          v-for="blog in blogs"
          :key="blog.id"
          class="mb-2 border-b pb-2"
        >  
          <RouterLink :to="`/blogs/${blog.id}`" class="text-blue-500 hover:underline">
            {{ blog.title }}
          </RouterLink>
          <div class="text-sm text-gray-500">
            投稿日: {{ moment(blog.created).format("YYYY年MM月DD日 HH:mm:ss") }}
          </div>
        </li>
      </ul>
    </div>
  </template>
  
  <script setup lang="ts">
  import { ref, onMounted } from "vue";
  import moment from "moment"

  
  const blogs = ref([]);
  
  
  const getBlogLists = async ()=>{
    const response = await fetch("http://localhost:8000/api/v1/blogs/");
    
    let results=await response.json();
    blogs.value = results["results"]
  };

  
  const init = async ()=>{
    await getBlogLists();
  };
    onMounted(() => {
        init();

  });
    
  </script>
  