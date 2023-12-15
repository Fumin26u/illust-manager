<script setup lang="ts">
import { ref } from 'vue'
import ApiManager from '@/server/apiManager'
import { apiPath } from '@/assets/ts/paths'

const directoryPath = ref<File | null>(null)
interface ImageInfo {
    imagePath: string
    class: string
    confidence: string
}
const imageInfo = ref<ImageInfo[]>([])

// 指定されたディレクトリ内の画像ファイルから画像リンク一覧を取得
const setImageInfo = (event: Event) => {
    const input = event.target as HTMLInputElement
    const files = input.files

    // バリデーション
    if (!files) return 'ファイルが選択されていません。'
    if (files.length === 0) return 'ファイルが空です。'

    Array.from(files).forEach((file) => {
        imageInfo.value.push({
            imagePath: URL.createObjectURL(file),
            class: '',
            confidence: '',
        })
    })
}

// blogの画像リンクをBASE64に変換
const convertImageToBase64 = async (imagePath: string) => {
    try {
        const response = await fetch(imagePath)
        const blob = await response.blob()
        const base64 = await new Promise((resolve, reject) => {
            const reader = new FileReader()
            reader.onload = () => resolve(reader.result)
            reader.onerror = () => reject(null)
            reader.readAsDataURL(blob)
        })
        return base64
    } catch (error) {
        console.error(error)
    }
}

// 信頼度をパーセンテージに変換
function formatPercentage(value: string) {
    const floatValue = parseFloat(value)
    const roundedValue = Math.round(floatValue * 100000) / 100000
    return (roundedValue * 100).toFixed(2) + '%'
}

const apiManager = new ApiManager()
const base64Images = ref<unknown[]>([])
// APIを介して画像を評価
const evaluateImage = async () => {
    // Extract only the imagePath from imageInfo and create a new array
    const imagePaths = imageInfo.value.map((info) => info.imagePath)

    // 画像を全てBASE64に変換
    base64Images.value = await Promise.all(
        imagePaths.map(
            async (imagePath) => await convertImageToBase64(imagePath)
        )
    )

    try {
        const response = await apiManager.post(`${apiPath}/api/evaluate`, {
            imagePaths: base64Images.value,
        })
        console.log(response.data)
        response.data.forEach((data: any, index: number) => {
            imageInfo.value[index].class = data.class
            imageInfo.value[index].confidence = formatPercentage(
                data.confidence
            )
        })
    } catch (error) {
        console.error(error)
    }
}
</script>

<template>
    <main id="page-evaluate">
        <div class="title-area">
            <h1 class="title">画像の評価</h1>
        </div>
        <div class="reference-form">
            <input type="file" webkitdirectory @change="setImageInfo" />
            <p v-if="directoryPath !== null">{{ directoryPath }}</p>
        </div>
        <div class="submit">
            <button @click="evaluateImage()">評価</button>
        </div>
        <dl class="image-info-list">
            <div v-for="(info, index) in imageInfo" :key="index">
                <dt>
                    <p>結果: {{ info.class !== '' ? info.class : '未評価' }}</p>
                    <p>
                        信頼度:
                        {{
                            info.confidence !== '' ? info.confidence : '未評価'
                        }}
                    </p>
                </dt>
                <dd><img :src="info.imagePath" /></dd>
            </div>
        </dl>
    </main>
</template>

<style scoped lang="scss">
@import '@/assets/scss/evaluate.scss';
</style>
