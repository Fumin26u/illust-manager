<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { CNN, Conv2d, MaxPooling2d } from '@/types/types/types'
import { createCnnInit, activations } from '@/assets/ts/train/cnn'
import { VDivider, VSwitch, VBtn, VIcon } from 'vuetify/components'
import { v4 as uuidv4 } from 'uuid'

const emit = defineEmits(['setCNN'])

// 各項目のタイトル
const titles = [
    '畳み込み層(Conv2D)',
    'プーリング層(MaxPooling2D)',
    'ドロップアウト',
]

// 各層のフォームをクリックした際、そのフォームにフォーカスを当てる
// フォーカスされたフォーム以外は値のみを表示
const focusedIndex = ref<number>(0)
const setFocusedIndex = (index: number) => {
    focusedIndex.value = index
}

const cnns = ref<CNN[]>([])
const addCNN = () => {
    const cnn = createCnnInit()
    cnn.uuid = uuidv4()

    cnns.value.push(cnn)
    focusedIndex.value = cnns.value.length - 1
}

const deleteCNN = (index: number) => {
    if (!confirm('削除しますか？')) return
    cnns.value.splice(index, 1)
}

// 完了ボタン押下時、設定したCNNを親コンポーネントに渡す
const doneCNNSettings = () => {
    emit('setCNN', cnns.value)
    focusedIndex.value = -1
}
// 編集ボタン押下時
const editCNNSettings = () => {
    focusedIndex.value = cnns.value.length - 1
}

onMounted(() => {
    addCNN()
})
</script>

<template>
    <div>
        <dl
            class="train-form cnn"
            v-for="(cnn, index) in cnns"
            :key="cnn.uuid"
            @click="setFocusedIndex(index)"
        >
            <v-divider
                :thickness="3"
                color="blue-lighten-4"
                class="border-opacity-100 divider"
            ></v-divider>
            <div class="hidden-form" v-if="focusedIndex !== index">
                <div>
                    <h4>畳み込み層</h4>
                    <div class="content">
                        <p v-for="(value, key) in cnn.conv2d" :key="key">
                            {{ key }}: {{ value }}
                        </p>
                    </div>
                </div>
                <div>
                    <h4>プーリング層</h4>
                    <div class="content">
                        <p v-for="(value, key) in cnn.maxPooling2d" :key="key">
                            {{ key }}: {{ value }}
                        </p>
                    </div>
                </div>
                <div>
                    <h4>ドロップアウト</h4>
                    <div class="content">
                        <p>Dropout: {{ cnn.dropout }}</p>
                    </div>
                </div>
            </div>
            <div class="display-form" v-else>
                <v-btn
                    color="red-darken-2"
                    class="vuetify-btn delete"
                    @click="deleteCNN(index)"
                >
                    <template v-slot:prepend>
                        <v-icon>mdi-delete</v-icon>
                    </template>
                    削除
                </v-btn>
                <div v-if="focusedIndex === index">
                    <div class="title">
                        <h4>畳み込み層(Conv2D)</h4>
                        <!-- <v-switch
                            color="primary"
                            :model-value="true"
                            class="detail-switch"
                            label="詳細設定"
                            hide-details
                        ></v-switch> -->
                    </div>
                    <div class="content">
                        <div>
                            <dt>filters</dt>
                            <dd>
                                <input
                                    type="number"
                                    v-model="cnn.conv2d.filters"
                                    min="16"
                                    step="16"
                                    max="512"
                                />
                            </dd>
                        </div>
                        <div>
                            <dt>kernel_size</dt>
                            <dd>
                                <input
                                    type="number"
                                    v-model="cnn.conv2d.kernel_size[0]"
                                    min="2"
                                    step="1"
                                    max="8"
                                />
                                x
                                <input
                                    type="number"
                                    v-model="cnn.conv2d.kernel_size[1]"
                                    min="2"
                                    step="1"
                                    max="8"
                                />
                            </dd>
                        </div>
                        <div>
                            <dt>activation</dt>
                            <dd>
                                <select v-model="cnn.conv2d.activation">
                                    <option
                                        v-for="activation in activations"
                                        :key="activation"
                                    >
                                        {{ activation }}
                                    </option>
                                </select>
                            </dd>
                        </div>
                        <div>
                            <dt>input_shape</dt>
                            <dd>
                                <input
                                    type="number"
                                    v-model="cnn.conv2d.input_shape[0]"
                                    min="120"
                                    step="1"
                                    max="720"
                                />
                                x
                                <input
                                    type="number"
                                    v-model="cnn.conv2d.input_shape[1]"
                                    min="120"
                                    step="1"
                                    max="720"
                                />
                                x
                                <input
                                    type="number"
                                    v-model="cnn.conv2d.input_shape[2]"
                                    min="2"
                                    step="1"
                                    max="12"
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
                <div>
                    <div class="title">
                        <h4>プーリング層(MaxPooling2D)</h4>
                    </div>
                    <div class="content">
                        <div class="pool-size">
                            <dt>pool_size</dt>
                            <dd>
                                <input
                                    type="number"
                                    v-model="cnn.maxPooling2d.pool_size[0]"
                                    min="1"
                                    step="1"
                                    max="12"
                                />
                                x
                                <input
                                    type="number"
                                    v-model="cnn.maxPooling2d.pool_size[1]"
                                    min="1"
                                    step="1"
                                    max="12"
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
                <div>
                    <h4>ドロップアウト</h4>
                    <div class="content">
                        <div>
                            <dt>Dropout</dt>
                            <dd>
                                <input
                                    type="number"
                                    v-model="cnn.dropout"
                                    min="0"
                                    step="0.05"
                                    max="0.5"
                                />
                            </dd>
                        </div>
                    </div>
                </div>
            </div>
        </dl>
        <v-btn
            color="blue-lighten-4"
            class="font-weight-bold vuetify-btn add"
            block
            @click="addCNN"
        >
            <template v-slot:prepend>
                <v-icon left>mdi-plus</v-icon>
            </template>
            追加
        </v-btn>
        <div class="form-cover" v-if="focusedIndex === -1"></div>
    </div>
    <v-btn
        color="green-darken-2"
        class="vuetify-btn done"
        @click="doneCNNSettings()"
        v-if="focusedIndex !== -1"
    >
        <template v-slot:prepend>
            <v-icon left>mdi-check</v-icon>
        </template>
        完了
    </v-btn>
    <v-btn
        color="blue-darken-2"
        class="vuetify-btn done"
        @click="editCNNSettings()"
        v-else
    >
        <template v-slot:prepend>
            <v-icon left>mdi-square-edit-outline</v-icon>
        </template>
        編集
    </v-btn>
</template>
