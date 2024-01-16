<script setup lang="ts">
import HeaderComponent from '@/components/HeaderComponent.vue'
import FileListComponent from '@/components/FileListComponent.vue'
import ButtonComponent from '@/components/ButtonComponent.vue'

import CNNComponent from '@/components/train/CNNComponent.vue'

import { ref, onMounted } from 'vue'
import { createCnnInit } from '@/assets/ts/train/cnn'
import ApiManager from '@/server/apiManager'
import { apiPath } from '@/assets/ts/paths'
import {
    EarlyStopping,
    ImageDataGenerator,
    TrainFlows,
    CNN,
    Dense,
    TrainModels,
    TrainParameters,
} from '@/types'

import { VBtn, VIcon } from 'vuetify/components'
import '@/assets/scss/train.scss'

const denses = ref<Dense[]>([
    {
        uuid: '',
        units: 256,
        activation: 'relu',
    },
])

const trainModels = ref<TrainModels>({
    batchNormalization: true,
    flatten: true,
    cnn: [],
    dense: [],
    final_dropout: 0.05,
})

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
        <div class="form-reference train-settings">
            <div class="train-overall">
                <h2>全体の設定</h2>
                <FileListComponent
                    title="データセット"
                    :type="'getImageDirs'"
                    @setSelectedFile="setSelectedFile"
                />
                <div>
                    <dt>試行回数(Epoch)</dt>
                    <dd><input type="number" /></dd>
                </div>
                <div>
                    <dt>最適化関数</dt>
                    <dd><input type="text" /></dd>
                </div>
            </div>
            <div>
                <h2>モデル構築</h2>
                <div class="train-models">
                    <h3>CNN (畳み込み・プーリング・ドロップアウト)</h3>
                    <CNNComponent />
                </div>
            </div>
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
