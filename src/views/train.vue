<script setup lang="ts">
import HeaderComponent from '@/components/HeaderComponent.vue'
import FileListComponent from '@/components/FileListComponent.vue'
import ButtonComponent from '@/components/ButtonComponent.vue'

import CNNComponent from '@/components/train/CNNComponent.vue'

import { ref } from 'vue'
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

const cnnComponents = ref<any>([])
const addCNNComponent = () => {
    cnnComponents.value.push(CNNComponent)
}

const cnns = ref<CNN[]>([])
const addCNN = (cnnInit: CNN) => {
    cnns.value.push(cnnInit)
}

const denses = ref<Dense[]>([
    {
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
        <div class="form-reference train-form">
            <dl class="input-form train-parameters">
                <h2>全体の設定</h2>
                <FileListComponent
                    title="参照画像を選択:"
                    :type="'getImageDirs'"
                    @setSelectedFile="setSelectedFile"
                />
                <div>
                    <dt>試行回数 (Epoch数)</dt>
                    <dd><input type="number" /></dd>
                </div>
                <div>
                    <dt>最適化関数</dt>
                    <dd><input type="text" /></dd>
                </div>
            </dl>
            <div class="train-models">
                <h2>各モデルの設定</h2>
                <dl class="input-form cnn">
                    <h3>CNN (畳み込み・プーリング・ドロップアウト)</h3>
                    <div
                        v-for="(cnnComponent, index) in cnnComponents"
                        :key="index"
                    >
                        <CNNComponent @addCNN="addCNN" />
                    </div>
                    <ButtonComponent
                        @click="addCNNComponent"
                        text="追加"
                        class="btn-small blue"
                    />
                </dl>
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
