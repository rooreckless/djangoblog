<template>
    <div>
        <h1>ブログ一覧</h1>
        <ul>
        <li v-for="blog in blogs" :key="blog.id">
            <router-link :to="`/blogs/${blog.id}`">{{ blog.title }}</router-link>
        </li>
        </ul>
    </div>
</template>

<script setup>
    import { ref, onMounted } from 'vue'

    const blogs = ref([])

    onMounted(async () => {
    const res = await fetch('https://localhost/api/v1/blogs/')
    blogs.value = await res.json()
    })
</script>
