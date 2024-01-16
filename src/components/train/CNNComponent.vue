<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { CNN, Conv2d, MaxPooling2d } from '@/types'
import { createCnnInit, activations } from '@/assets/ts/train/cnn'
import { VDivider, VSelect, VBtn, VIcon } from 'vuetify/components'
import { v4 as uuidv4 } from 'uuid'

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

onMounted(() => {
    addCNN()
})
</script>

<template>
    <dl
        class="train-form cnn"
        v-for="(cnn, index) in cnns"
        :key="cnn.uuid"
        @click="setFocusedIndex(index)"
    >
        <v-divider
            :thickness="3"
            color="info"
            class="border-opacity-50 divider"
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
                <p>ドロップアウト: {{ cnn.dropout }}</p>
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
                <h4>畳み込み層(Conv2D)</h4>
                <div class="content">
                    <div class="filters">
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
                    <div v-if="cnn.conv2d.input_shape !== undefined">
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
                                min="120"
                                step="1"
                                max="720"
                            />
                        </dd>
                    </div>
                </div>
            </div>
            <div>
                <h4>プーリング層(MaxPooling2d)</h4>
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
    <v-btn color="green-darken-2" class="vuetify-btn done">
        <template v-slot:prepend>
            <v-icon left>mdi-check</v-icon>
        </template>
        完了
    </v-btn>
</template>
