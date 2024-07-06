<script setup lang="ts">
import HeaderComponent from '@/components/HeaderComponent.vue'
import FileListComponent from 'backup/FileListComponent.vue'

import CNNComponent from '@/components/train/CNNComponent.vue'
import DenseComponent from '@/components/train/DenseComponent.vue'

import { ref, onMounted } from 'vue'
import ApiManager from '@/server/apiManager'
import { apiPath } from '@/assets/ts/paths'
import optimizers from '@/assets/ts/train/optimizers'
import { monitors, modes } from '@/assets/ts/train/earlyStopping'
import {
    ImageDataGenerator,
    TrainFlows,
    DataSets,
    CNN,
    Dense,
    TrainModels,
    TrainParameters,
} from '@/types/types/types'

import { VBtn, VIcon, VDivider, VSwitch } from 'vuetify/components'
import '@/assets/scss/train.scss'

const isSetDetail = ref<boolean>(false)

/* -----------------  

    データ拡張

----------------- */
const imageDataGenerator = ref<ImageDataGenerator>({
    rescale: 1,
    shear_range: 0,
    zoom_range: 0.2,
    horizontal_flip: false,
    validation_split: 0.2,
})

const trainFlows = ref<TrainFlows>({
    resize_resolution: [224, 224],
    batch_size: 32,
    class_mode: 'categorical',
})

const datasetPath = ref<string>('')
// モデルと参照画像フォルダを設定
const setDatasetPath = (
    type: 'getModels' | 'getImageDirs',
    selected: string
) => {
    datasetPath.value = selected
}

/* -----------------  

    モデル訓練

----------------- */
const trainParameters = ref<TrainParameters>({
    epochs: 32,
    optimizer: 'adam',
    isSetEarlyStopping: true,
    earlyStopping: {
        monitor: 'val_loss',
        patience: 8,
        verbose: 1,
        mode: 'auto',
        restore_best_weights: true,
    },
})

const trainModels = ref<TrainModels>({
    batchNormalization: true,
    flatten: true,
    cnn: [],
    dense: [],
    final_dropout: 0.05,
})

// 子コンポーネント内のCNNを取得
const cnns = ref<CNN[]>([])
const setCNN = (provided: CNN[]) => {
    cnns.value = provided
}

// 子コンポーネント内のDenseを取得
const denses = ref<Dense[]>([])
const setDense = (provided: Dense[]) => {
    denses.value = provided
}

/* -----------------  

    訓練の実行

----------------- */
const apiManager = new ApiManager()
// フォーム値のパラメータをAPI送信用に整形
// データセット
const createDataSets = (): DataSets => {
    return {
        trainFlows: trainFlows.value,
        imageDataGenerator: imageDataGenerator.value,
    }
}
// 訓練モデル
const createTrainModels = (model: TrainModels) => {
    const newTrainModels = { ...model }
    newTrainModels.cnn = cnns.value
    newTrainModels.dense = denses.value
    return newTrainModels
}

const messages = ref<{ content: string; error: boolean }[]>([])
const train = async () => {
    messages.value = []

    // 詳細設定がoffの場合パスだけ送信
    if (!isSetDetail.value) {
        try {
            const response = await apiManager.post(`${apiPath}/train/train`, {
                path: datasetPath.value,
                train_parameter: trainParameters.value,
                isSetDetail: false,
            })
            messages.value.push({
                content: response.content,
                error: response.error,
            })
        } catch (error) {
            console.error(error)
        }
    }

    // 詳細設定がonの場合
    // バリデーション
    if (cnns.value.length === 0) {
        messages.value.push({
            content: 'CNNの設定を完了してください。',
            error: true,
        })
        return
    }
    if (denses.value.length === 0) {
        messages.value.push({
            content: 'Denseの設定を完了してください。',
            error: true,
        })
        return
    }

    // 各パラメータを整形
    const datasets = createDataSets()
    const models = createTrainModels(trainModels.value)

    const postData = {
        path: datasetPath.value,
        isSetDetail: true,
        dataset: datasets,
        train_model: models,
        train_parameter: trainParameters.value,
    }

    try {
        const response = await apiManager.post(
            `${apiPath}/train/train`,
            postData
        )
        messages.value.push({
            content: response.content,
            error: response.error,
        })
    } catch (error) {
        console.error(error)
    }
}
</script>

<template>
    <HeaderComponent />
    <main id="page-train">
        <div class="title-area">
            <h1 class="title">画像訓練</h1>
            <div class="main-settings">
                <FileListComponent
                    title="データセットのパス"
                    :type="'getImageDirs'"
                    @setSelectedFile="setDatasetPath"
                />
                <v-switch
                    v-model="isSetDetail"
                    label="詳細設定"
                    hide-details
                    color="primary"
                ></v-switch>
            </div>
        </div>
        <div class="train-generator" v-if="isSetDetail">
            <h2>データ拡張</h2>
            <div class="flowFromDirectory">
                <h3>データセット</h3>
                <div>
                    <div>
                        <dt>リサイズ時の解像度</dt>
                        <dd>
                            <input
                                type="number"
                                v-model="trainFlows.resize_resolution[0]"
                                min="120"
                                step="1"
                                max="720"
                            />
                            x
                            <input
                                type="number"
                                v-model="trainFlows.resize_resolution[1]"
                                min="120"
                                step="1"
                                max="720"
                            />
                        </dd>
                    </div>
                    <div>
                        <dt>バッチサイズ</dt>
                        <dd>
                            <input
                                type="number"
                                v-model="trainFlows.batch_size"
                                min="16"
                                step="8"
                                max="128"
                            />
                        </dd>
                    </div>
                </div>
            </div>
            <div class="image-data-generator">
                <h3>拡張設定</h3>
                <div>
                    <div>
                        <dt>rescale</dt>
                        <dd>
                            <input
                                type="number"
                                v-model="imageDataGenerator.rescale"
                                min="120"
                                step="1"
                                max="255"
                            />
                            / 255
                        </dd>
                    </div>
                    <div>
                        <dt>shear_range</dt>
                        <dd>
                            <input
                                type="number"
                                v-model="imageDataGenerator.shear_range"
                                min="0"
                                step="0.05"
                                max="1"
                            />
                        </dd>
                    </div>
                    <div>
                        <dt>zoom_range</dt>
                        <dd>
                            <input
                                type="number"
                                v-model="imageDataGenerator.zoom_range"
                                min="0"
                                step="0.05"
                                max="1"
                            />
                        </dd>
                    </div>
                    <div>
                        <dt>
                            <label for="horizontal_flip">horizontal_flip</label>
                        </dt>
                        <dd>
                            <input
                                type="checkbox"
                                v-model="imageDataGenerator.horizontal_flip"
                                id="horizontal_flip"
                            />
                        </dd>
                    </div>
                    <div>
                        <dt>validation_split</dt>
                        <dd>
                            <input
                                type="number"
                                v-model="imageDataGenerator.validation_split"
                                min="0"
                                step="0.05"
                                max="0.5"
                            />
                        </dd>
                    </div>
                </div>
            </div>
            <v-divider
                :thickness="2"
                color="green-lighten-4"
                class="border-opacity-100 divider short"
            ></v-divider>
        </div>
        <div class="train-settings" v-if="isSetDetail">
            <h2>モデル訓練</h2>
            <div class="train-parameters">
                <h3>
                    訓練時の
                    <br />
                    パラメータ
                </h3>
                <div>
                    <div>
                        <dt>試行回数(Epoch)</dt>
                        <dd>
                            <input
                                type="number"
                                v-model="trainParameters.epochs"
                                min="10"
                                step="1"
                                max="128"
                            />
                        </dd>
                    </div>
                    <div>
                        <dt>最適化関数(Optimizer)</dt>
                        <dd>
                            <select v-model="trainParameters.optimizer">
                                <option
                                    v-for="optimizer in optimizers"
                                    :key="optimizer"
                                >
                                    {{ optimizer }}
                                </option>
                            </select>
                        </dd>
                    </div>
                </div>
            </div>
            <div class="train-models">
                <h3>モデル構築</h3>
                <div>
                    <div class="batch-normalization">
                        <dt>
                            <label for="batch-normalization">
                                バッチ正規化 (BatchNormalization)
                            </label>
                        </dt>
                        <dd>
                            <input
                                type="checkbox"
                                v-model="trainModels.batchNormalization"
                                id="batch-normalization"
                            />
                        </dd>
                    </div>
                    <div class="flatten">
                        <dt>
                            <label for="flatten">平坦化 (Flatten)</label>
                        </dt>
                        <dd>
                            <input
                                type="checkbox"
                                v-model="trainModels.flatten"
                                id="flatten"
                            />
                        </dd>
                    </div>
                    <div class="final_dropout">
                        <dt>
                            <label for="final_dropout">最終Dropout値</label>
                        </dt>
                        <dd>
                            <input
                                type="number"
                                v-model="trainModels.final_dropout"
                                id="final_dropout"
                                min="0"
                                step="0.05"
                                max="0.5"
                            />
                        </dd>
                    </div>
                </div>
            </div>
            <div
                class="early-stopping"
                :style="
                    !trainParameters.isSetEarlyStopping
                        ? 'align-items:flex-start;'
                        : ''
                "
            >
                <div class="title">
                    <h3>EarlyStopping</h3>
                    <v-switch
                        v-model="trainParameters.isSetEarlyStopping"
                        hide-details
                        color="primary"
                    ></v-switch>
                </div>
                <div v-if="trainParameters.isSetEarlyStopping">
                    <div>
                        <dt>monitor</dt>
                        <dd>
                            <select
                                v-model="trainParameters.earlyStopping.monitor"
                            >
                                <option
                                    v-for="monitor in monitors"
                                    :key="monitor"
                                >
                                    {{ monitor }}
                                </option>
                            </select>
                        </dd>
                    </div>
                    <div>
                        <dt>patience</dt>
                        <dd>
                            <input
                                type="number"
                                v-model="trainParameters.earlyStopping.patience"
                                id="final_dropout"
                                min="4"
                                step="1"
                                max="16"
                            />
                        </dd>
                    </div>
                    <div>
                        <dt>進捗の出力</dt>
                        <dd>
                            <input
                                type="radio"
                                v-model="trainParameters.earlyStopping.verbose"
                                id="verbose_0"
                                value="0"
                            />
                            <label for="verbose_0">出力なし</label>
                            <input
                                type="radio"
                                v-model="trainParameters.earlyStopping.verbose"
                                id="verbose_1"
                                value="1"
                            />
                            <label for="verbose_1">進捗バー</label>
                            <input
                                type="radio"
                                v-model="trainParameters.earlyStopping.verbose"
                                id="verbose_2"
                                value="2"
                            />
                            <label for="verbose_2">各行出力</label>
                        </dd>
                    </div>
                    <div>
                        <dt>mode</dt>
                        <dd>
                            <select
                                v-model="trainParameters.earlyStopping.mode"
                            >
                                <option v-for="mode in modes" :key="mode">
                                    {{ mode }}
                                </option>
                            </select>
                        </dd>
                    </div>
                    <div>
                        <dt>
                            <label for="restore_best_weights">
                                restore_best_weights
                            </label>
                        </dt>
                        <dd>
                            <input
                                type="checkbox"
                                v-model="
                                    trainParameters.earlyStopping
                                        .restore_best_weights
                                "
                                id="restore_best_weights"
                            />
                        </dd>
                    </div>
                </div>
                <div v-else :style="'margin: 1em 0 0 3em'">設定しない</div>
            </div>
            <v-divider
                :thickness="2"
                color="green-lighten-4"
                class="border-opacity-100 divider short"
            ></v-divider>
            <div class="train-cnn">
                <h3>CNN (畳み込み・プーリング・ドロップアウト)</h3>
                <div>
                    <CNNComponent @setCNN="setCNN" />
                </div>
            </div>
            <div class="train-dense">
                <h3>Dense (結合層)</h3>
                <div>
                    <DenseComponent @setDense="setDense" />
                </div>
            </div>
        </div>
        <div class="button-area input-form" v-if="datasetPath !== ''">
            <v-btn
                color="blue-darken-4"
                class="vuetify-btn execute font-weight-bold"
                @click="train"
            >
                <template v-slot:prepend>
                    <v-icon left>mdi-ray-start-arrow</v-icon>
                </template>
                実行
            </v-btn>
            <div v-for="(message, index) in messages" :key="index">
                <p :style="message.error ? 'color: red;' : ''">
                    {{ message.content }}
                </p>
            </div>
        </div>
    </main>
</template>
