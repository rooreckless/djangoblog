<!-- BlogCreate.vue（簡易例） -->
<template>
<div class="container mx-auto px-4 py-8">
    <h1 class="text-2xl font-bold mb-4">ブログ作成</h1>
    <form @submit.prevent="submitBlog" class="">
        <!-- formタグの記述内容は https://qiita.com/koinunopochi/items/cdff29b65a5f26224e95 -->
        <!-- https://qiita.com/shizen-shin/items/33845020453b0af6ebde -->
        <!-- 今回は「submitなボタンを押された時にバリデーションチェックに成功したらsubmitBlog関数を実行する」の意味 -->
        <h2 class="text-xl font-semibold">ブログタイトル</h2>
        <!-- ↓のinputに入れられた文字は v-modelに指定した変数に入る -->
        <input data-testid="blogcreate-input-title" class=" mb-4 p-4 rounded-xl shadow bg-white border w-full" v-model="title" placeholder="タイトル"/>
        <p v-if="form_errors.title" class="text-red-500" data-testid="blogcreate-input-title-error">{{ form_errors.title }}</p>
        <h2 class="text-xl font-semibold">本文</h2>
        <!-- ↓のtextareaに入れられた文字は v-modelに指定した変数に入る -->
        <textarea data-testid="blogcreate-textarea-contents-text" class="mb-2 p-4 rounded-xl shadow bg-white border w-full" v-model="contents_text" placeholder="本文"/>
        <p v-if="form_errors.contents_text" class="text-red-500" data-testid="blogcreate-textarea-contents-text-error">{{ form_errors.contents_text }}</p>
        <div class="mt-6 mx-4 flex justify-between items-center space-x-4">   
            <!-- 戻るボタン -->
            <AppTrasitionPageButton to="/blogs" data-testid="blogcreate-back-btn">
                ブログ一覧画面へ戻る
            </AppTrasitionPageButton>

            <!-- 作成ボタン このボタンが押されることでsubmitイベントが発火 = formタグは「submitイベント発火時はsubmitBlog実施」状態になっているのでバックエンドへPOSTリクエストされる -->
            <button
                type="submit"
                :disabled="!isFormValid"
                :class="[
                    'px-4 py-2 rounded',
                    isFormValid ? 'bg-sky-400 hover:bg-gray-300' : 'bg-gray-100 cursor-not-allowed',
                ]"
                data-testid="blogcreate-submit-btn"
                >
                作成
            </button>

        </div>
        
    </form>
    <p v-if="errorMessage" data-testid="blogcreate-backend-error-message" class="error">{{ errorMessage }}</p>
</div>
</template>
  

<script setup lang="ts">
import { ref, computed } from "vue"
import { useRouter } from "vue-router"
import { useForm, useField } from 'vee-validate'
import * as yup from 'yup'

// スキーマ定義=フォーム内パーツのバリデーションルールを定義し、yup ライブラリを使用してスキーマを作成
// titleについては、必須項目であること、最大文字数200文字であることを指定
// contents_textについては、必須項目であることを指定
const schema = yup.object({
  title: yup
    .string()
    .required('タイトルは必須です')
    .max(200, 'タイトルは200文字以内で入力してください'),
  contents_text: yup
    .string()
    .required('本文は必須です'),
})

// useForm にスキーマ=↑で決めたフォームバリデーションルールのyupをを渡す
// 
const { handleSubmit, errors :form_errors } = useForm({
  validationSchema: schema
})

// 各フィールドを useField で接続
// {value: title}のtitleは、v-modelで使用できるようになる。useField('title')の方はschemaｍのyup.objectに入れたオブジェクトのことを指す
const { value: title} = useField('title')
const { value: contents_text} = useField('contents_text')
// useFieldで定義しているので、v-modelで双方バインディングする変数は作成しなくていい。
// const title = ref("")
// const contentsText = ref("")
const errorMessage = ref("")
const router = useRouter()

const submitBlog = handleSubmit (async (form_values) => {
    console.log("form_values=",form_values);
    try {
        // バックエンドへPOSTリクエスト 第2引数がオブジェクトで、バックエンドへ渡す内容
        // オブジェクトのbodyについては、「refで定義した変数 = フォームのinputやtextareaの記述内容」からオブジェクトを作成 → 「JSON.stringifyで文字列化した結果」がbodyの値になっている
        const response = await fetch("http://localhost:8000/api/v1/blogs/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                // title: title.value,
                // contents_text: contentsText.value,
                title: form_values.title,
                contents_text: form_values.contents_text,
            }),
        })

        if (!response.ok) {
            const errorData = await response.json();
            
            if (errorData.detail) {
                errorMessage.value = errorData.detail;
            } else {
                // 複数フィールドのバリデーションエラーをまとめて表示する例（必要に応じて整形）
                errorMessage.value = Object.values(errorData).flat().join("／");
            }
            return;
        }

        // 成功時は一覧ページにリダイレクト（必要に応じて）
        backBlogListPage();
    } catch (error) {
        errorMessage.value = "ネットワークエラーが発生しました"
    }
}, (errors)=>{
    console.log("バリデーションエラー",errors);
    // バリデーションエラーが発生した場合の処理
    // 例: エラーメッセージを表示するなど
  }

);

// methods

const backBlogListPage = ()=>{
    console.log("--戻るボタン--")
    router.push('/blogs')  // 一覧画面に戻る
};

// computed
// フォーム内の要素に値が入っている = 必須入力項目に値が入っているかどうかを算出する
const isFormValid = computed(() => {
    // isFormValidの値は、入力欄のtitleとcontents_textの双方に値が入っているなら、Trueになる。
    // Trueになると、作成ボタンには:disabled="!isFormValid"が記述されているので、作成ボタンが押せるようになる
    return title.value && contents_text.value
})

// - フロントエンドのcomputedは、ユーザーの画面操作によって「画面描画にのみ」影響を及ぼしたい場合使う(例:フロントバリデーションエラーなら、ボタンをdisabledで押せなくする、や、色を変える、など)
// - 一方、ref + watchは、ユーザーの画面操作によって「他の内部処理を実行したり、apiへリクエストを行ったりする必要がある」場合に使う(例:フロントの検索欄に、1文字入力するたびに、バックエンドへ検索を行う(=インクリメンタルサーチ)や、ログ出力など)

</script>

