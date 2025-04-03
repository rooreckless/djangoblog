<template>
    <div v-if="blog">
      <h1>{{ blog.title }}</h1>
      <p>{{ blog.contents_text }}</p>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue'
  import { useRoute } from 'vue-router'
  
  const route = useRoute()
  const blog = ref(null)
  
  onMounted(async () => {
    const res = await fetch(`https://localhost/api/v1/blogs/${route.params.id}/`)
    blog.value = await res.json()
  })
  </script>
  