<script setup lang="ts">
import HeaderComponent from '@/components/HeaderComponent.vue'
import FileSelectComponent from '@/components/FileSelectComponent.vue'
import ButtonComponent from '@/components/ButtonComponent.vue'

import { ref } from 'vue'
import ApiManager from '@/server/apiManager'
import { apiPath } from '@/assets/ts/paths'
import { ImageInfo } from '@/types'

const imageInfo = ref<ImageInfo[]>([])
// 1度にAPIに送るリクエスト数
const batchSize = 50

// ディレクトリ選択時、画像情報一覧を取得
const setImageInfo = (selectedImageInfo: ImageInfo[]) => {
    imageInfo.value = selectedImageInfo
}

// blobの画像リンクをBASE64に変換
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

// 実行ボタン押下時、画像データを切り抜きAPIに送信
const apiManager = new ApiManager()
const cropImage = async () => {
    const imagePaths = await Promise.all(
        imageInfo.value.map(async (info) => {
            return {
                childDir: info.childDir,
                imageInfo: await convertImageToBase64(info.imagePath),
            }
        })
    )

    try {
        for (let i = 0; i < imagePaths.length; i += batchSize) {
            const batch = imagePaths.slice(i, i + batchSize)
            const response = await apiManager.post(
                `${apiPath}/crop/cropImage`,
                {
                    content: batch,
                }
            )
            console.log(response, `${i + batchSize}`)
        }
    } catch (error) {
        console.error(error)
    }
}
</script>

<template>
    <HeaderComponent />
    <main id="page-evaluate">
        <div class="title-area">
            <h1 class="title">画像の切り抜き</h1>
        </div>
        <dl class="form-reference input-form">
            <FileSelectComponent
                title="画像フォルダを選択:"
                @setImageInfo="setImageInfo"
            />
        </dl>
        <div class="button-area input-form" v-if="imageInfo.length > 0">
            <ButtonComponent
                @click="cropImage"
                text="実行"
                :buttonClass="'btn-common blue'"
            />
        </div>
    </main>
</template>
