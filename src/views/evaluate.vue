<script setup lang="ts">
import FileListComponent from '@/components/FileListComponent.vue'
import FileSelectComponent from '@/components/FileSelectComponent.vue'
import ButtonComponent from '@/components/ButtonComponent.vue'
import HeaderComponent from '@/components/HeaderComponent.vue'

import { ref } from 'vue'
import ApiManager from '@/server/apiManager'
import { apiPath } from '@/assets/ts/paths'
import { ImageInfo, EvaluatedResult } from '@/types'
import '@/assets/scss/evaluate.scss'

const isEvaluated = ref<boolean>(false)
const imageInfo = ref<ImageInfo[]>([])
const evaluatedResult = ref<EvaluatedResult[][]>([])
const minConfidence = ref<number>(50)

const selectedModel = ref<string>('')
const selectedImageDir = ref<string>('')

// ディレクトリ選択時、画像情報一覧を取得
const setImageInfo = (selectedImageInfo: ImageInfo[]) => {
    imageInfo.value = selectedImageInfo
}

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
        console.log(selectedModel.value, selectedImageDir.value)
        const response = await apiManager.post(`${apiPath}/api/evaluate`, {
            imagePaths: base64Images.value,
            model: selectedModel.value,
            imageDir: selectedImageDir.value,
        })

        response.data.forEach(
            (result: EvaluatedResult[] | false, index: number) => {
                if (result === false) {
                    imageInfo.value.splice(index, 1)
                } else {
                    evaluatedResult.value.push(result)
                    imageInfo.value[index].className = result[0].className
                    imageInfo.value[index].confidence = result[0].probability
                }
            }
        )

        isEvaluated.value = true
    } catch (error) {
        console.error(error)
    }
}

// 画像のソート
const sortImageInfo = (method: string) => {
    if (method === 'name') {
        imageInfo.value.sort((a, b) => {
            if (a.className < b.className) {
                return -1
            }
            if (a.className > b.className) {
                return 1
            }
            return 0
        })
    } else if (method === 'index') {
        imageInfo.value.sort((a, b) => a.index - b.index)
    }
}

const selectClass = (index: number) => {
    const selectedClassName = imageInfo.value[index].className
    imageInfo.value[index].confidence = evaluatedResult.value[index].find(
        (result) => result.className === selectedClassName
    )?.probability
    console.log(imageInfo.value[index])
}

// 画像をキャラクター毎にフォルダ分けして保存
const saveImage = async () => {
    const imageInfo_base64 = await Promise.all(
        imageInfo.value.map(async ({ imagePath, ...rest }) => ({
            imagePath: await convertImageToBase64(imagePath),
            ...rest,
        }))
    )

    try {
        const response = await apiManager.post(`${apiPath}/api/save`, {
            minConfidence: minConfidence.value,
            imageInfo: imageInfo_base64,
        })
        console.log(response)
    } catch (error) {
        console.error(error)
    }
}
</script>

<template>
    <HeaderComponent />
    <main id="page-evaluate">
        <div class="title-area">
            <h1 class="title">画像の評価</h1>
        </div>
        <dl class="form-reference input-form">
            <FileSelectComponent
                title="画像フォルダを選択:"
                @setImageInfo="setImageInfo"
            />
        </dl>
        <div
            class="button-area input-form"
            v-if="!isEvaluated && imageInfo.length > 0"
        >
            <FileListComponent
                title="モデルを選択:"
                :type="'getModels'"
                @setSelectedFile="setSelectedFile"
            />
            <FileListComponent
                title="参照画像を選択:"
                :type="'getImageDirs'"
                @setSelectedFile="setSelectedFile"
            />
            <ButtonComponent
                @click="evaluateImage"
                text="評価"
                :buttonClass="'btn-common blue'"
            />
        </div>
        <div v-if="isEvaluated">
            <div class="evaluated-detail">
                <p>
                    評価結果が正しくない場合、選択ボックスから正しいキャラクターを選択してください。
                </p>
                <input
                    type="number"
                    step="0.5"
                    min="10"
                    max="90"
                    v-model="minConfidence"
                />
                <span>
                    %以上の信頼度を保存
                    (それ以下の場合、その他フォルダに保存されます。)
                </span>
            </div>
            <div class="button-area">
                <ButtonComponent
                    @click="sortImageInfo('name')"
                    text="名前でソート"
                    :buttonClass="'btn-common blue'"
                />
                <ButtonComponent
                    @click="sortImageInfo('index')"
                    text="元に戻す"
                    :buttonClass="'btn-common red'"
                />
                <ButtonComponent
                    @click="saveImage()"
                    text="保存"
                    :buttonClass="'btn-common green'"
                />
            </div>
        </div>
        <dl class="image-info-list">
            <div v-for="(info, index) in imageInfo" :key="index">
                <dt>
                    <div v-if="isEvaluated">
                        <select
                            v-model="info.className"
                            @change="selectClass(index)"
                        >
                            <option
                                v-for="(evaluation, index_2) in evaluatedResult[
                                    index
                                ]"
                                :key="index_2"
                            >
                                {{ evaluation.className }}
                            </option>
                        </select>
                        <p>信頼度: {{ info.confidence }}</p>
                        <input
                            type="checkbox"
                            v-model="info.isImportant"
                            :id="`is-important-${index}`"
                        />
                        <label :for="`is-important-${index}`">
                            確実に保存する
                        </label>
                    </div>
                    <p v-else>未評価</p>
                </dt>
                <dd><img :src="info.imagePath" /></dd>
            </div>
        </dl>
    </main>
</template>
