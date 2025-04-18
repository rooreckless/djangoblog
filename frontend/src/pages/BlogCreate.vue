<!-- BlogCreate.vue（簡易例） -->
<template>
<div class="container mx-auto px-4 py-8">
    <h1 class="text-2xl font-bold mb-4">ブログ作成</h1>
    <form @submit.prevent="submitBlog" class="">
        <!-- formタグの記述内容は https://qiita.com/koinunopochi/items/cdff29b65a5f26224e95 -->
        <!-- https://qiita.com/shizen-shin/items/33845020453b0af6ebde -->
        <h2 class="text-xl font-semibold">ブログタイトル</h2>
        <!-- ↓のinputに入れられた文字は v-modelに指定した変数に入る -->
        <input data-testid="blogcreate-input-title" class=" mb-4 p-4 rounded-xl shadow bg-white border w-full" v-model="title" placeholder="タイトル" required />
        <h2 class="text-xl font-semibold">本文</h2>
        <!-- ↓のtextareaに入れられた文字は v-modelに指定した変数に入る -->
        <textarea data-testid="blogcreate-textarea-contents-text" class="mb-2 p-4 rounded-xl shadow bg-white border w-full" v-model="contentsText" placeholder="本文" required />
        
        <div class="mt-6 mx-4 flex justify-between items-center space-x-4">
            <button
            type="button"
            class="px-4 py-2 rounded bg-gray-200 hover:bg-gray-300"
            @click="backBlogListPage"
            data-testid="blogcreate-back-btn"
            >
            <!-- 戻るボタン -->
            戻る
            </button>

            <button type="submit" data-testid="blogcreate-submit-btn" class="px-4 py-2 rounded bg-gray-200 hover:bg-gray-300">
            <!-- 作成ボタン このボタンが押されることでsubmitイベントが発火 = formタグは「submitイベント発火時はsubmitBlog実施」状態になっているのでバックエンドへPOSTリクエストされる -->
                作成
            </button>
        </div>
        
    </form>
    <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
</div>
</template>
  

<script setup lang="ts">
import { ref } from "vue"
import { useRouter } from "vue-router"

const title = ref("")
const contentsText = ref("")
const errorMessage = ref("")
const router = useRouter()

const submitBlog = async () => {
    try {
        // バックエンドへPOSTリクエスト 第2引数がオブジェクトで、バックエンドへ渡す内容
        // オブジェクトのbodyについては、「refで定義した変数 = フォームのinputやtextareaの記述内容」からオブジェクトを作成 → 「JSON.stringifyで文字列化した結果」がbodyの値になっている
        const response = await fetch("http://localhost:8000/api/v1/blogs/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                title: title.value,
                contents_text: contentsText.value,
            }),
        })

        if (!response.ok) {
            // 
            const errorData = await response.json()
            errorMessage.value = errorData?.detail || "作成に失敗しました"
            return
        }

        // 成功時は一覧ページにリダイレクト（必要に応じて）
        router.push("/blogs/")
    } catch (error) {
        errorMessage.value = "ネットワークエラーが発生しました"
    }
}

const backBlogListPage = ()=>{
  console.log("--戻るボタン--")
  router.push('/blogs')  // 一覧画面に戻る
};

</script>

