<script setup lang="ts">
import { ref } from 'vue'
import ApiManager from '@/server/apiManager'
import { apiPath } from '@/assets/ts/paths'

const directoryPath = ref<File | null>(null)
const imagePaths = ref<string[]>([])

// 指定されたディレクトリ内の画像ファイルから画像リンク一覧を取得
const setImagePaths = (event: Event) => {
    const input = event.target as HTMLInputElement
    const files = input.files

    // バリデーション
    if (!files) return 'ファイルが選択されていません。'
    if (files.length === 0) return 'ファイルが空です。'

    imagePaths.value = Array.from(files).map((file) =>
        URL.createObjectURL(file)
    )
}

const apiManager = new ApiManager()
const getDirectory = async () => {
    const formData = new FormData()
    // フォルダ内の1つ目のファイルの相対パスをフォームに挿入
    // formData.append('firstFilePath', files[0].webkitRelativePath)
    // console.log(files[0])

    try {
        const response = await apiManager.get(
            `${apiPath}/api/getDirectory`,
            formData
        )
        console.log(response)
    } catch (error) {
        console.error(error)
    }
}
</script>

<template>
    <section id="page-evaluate">
        <div class="title-area">
            <h1 class="title">画像の評価</h1>
        </div>
        <div class="reference-form">
            <input type="file" webkitdirectory @change="setImagePaths" />
            <p v-if="directoryPath !== null">{{ directoryPath }}</p>
        </div>
        <div v-for="(imagePath, index) in imagePaths" :key="index">
            <img :src="imagePath" />
        </div>
    </section>
</template>
