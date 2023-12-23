<script setup lang="ts">
import HeaderComponent from '@/components/HeaderComponent.vue'
import FileListComponent from '@/components/FileListComponent.vue'
import ButtonComponent from '@/components/ButtonComponent.vue'

import { ref } from 'vue'
import ApiManager from '@/server/apiManager'
import { apiPath } from '@/assets/ts/paths'
import getCurrentTime from '@/assets/ts/getCurrentTime'

const selectedModel = ref<string>('')
const selectedImageDir = ref<string>('')
// モデルと参照画像フォルダを設定
const setSelectedFile = (
    type: 'getModels' | 'getImageDirs',
    selected: string
) => {
    if (type === 'getModels') {
        selectedModel.value = selected
    } else if (type === 'getImageDirs') {
        selectedImageDir.value = selected
    }
}

// 実行ボタン押下時、画像データを切り抜きAPIに送信
const apiManager = new ApiManager()
const train = async () => {
    try {
        const response = await apiManager.post(`${apiPath}/train/train`, {
            path: selectedImageDir.value,
        })
    } catch (error) {
        console.error(error)
    }
}
</script>

<template>
    <HeaderComponent />
    <main id="page-evaluate">
        <div class="title-area">
            <h1 class="title">画像訓練</h1>
        </div>
        <div class="form-reference input-form">
            <FileListComponent
                title="参照画像を選択:"
                :type="'getImageDirs'"
                @setSelectedFile="setSelectedFile"
            />
        </div>
        <div class="button-area input-form" v-if="selectedImageDir !== ''">
            <ButtonComponent
                @click="train"
                text="実行"
                :buttonClass="'btn-common blue'"
            />
        </div>
    </main>
</template>
