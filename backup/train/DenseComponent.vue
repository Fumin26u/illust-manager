<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { Dense } from '@/types/types/types'
import { createDenseInit, activations } from '@/assets/ts/train/dense'
import { VDivider, VCheckbox, VBtn, VIcon } from 'vuetify/components'
import { v4 as uuidv4 } from 'uuid'

const emit = defineEmits(['setDense'])

// 各層のフォームをクリックした際、そのフォームにフォーカスを当てる
// フォーカスされたフォーム以外は値のみを表示
const focusedIndex = ref<number>(0)
const setFocusedIndex = (index: number) => {
    focusedIndex.value = index
}

const denses = ref<Dense[]>([])
const addDense = () => {
    const dense = createDenseInit()
    dense.uuid = uuidv4()

    denses.value.push(dense)
    focusedIndex.value = denses.value.length - 1
}

const deleteDense = (index: number) => {
    if (!confirm('削除しますか？')) return
    denses.value.splice(index, 1)
}

// 完了ボタン押下時、設定したdenseを親コンポーネントに渡す
const doneDenseSettings = () => {
    // データセットのフォルダ数を使用する場合、unitsをclass_lengthに変更
    denses.value.forEach((dense) => {
        if (dense.isUsingClassLength) {
            dense.units = 'class_length'
        }
    })

    emit('setDense', denses.value)
    focusedIndex.value = -1
}
// 編集ボタン押下時
const editDenseSettings = () => {
    focusedIndex.value = denses.value.length - 1
}

onMounted(() => {
    addDense()
})
</script>

<template>
    <div>
        <dl
            class="train-form dense"
            v-for="(dense, index) in denses"
            :key="dense.uuid"
            @click="setFocusedIndex(index)"
        >
            <v-divider
                :thickness="3"
                color="blue-lighten-4"
                class="border-opacity-100 divider"
            ></v-divider>
            <div class="hidden-form" v-if="focusedIndex !== index">
                <div>
                    <h4>結合層</h4>
                    <div class="content">
                        <p>units: {{ dense.units }}</p>
                        <p>activation: {{ dense.activation }}</p>
                    </div>
                </div>
            </div>
            <div class="display-form" v-else>
                <v-btn
                    color="red-darken-2"
                    class="vuetify-btn delete"
                    @click="deleteDense(index)"
                >
                    <template v-slot:prepend>
                        <v-icon>mdi-delete</v-icon>
                    </template>
                    削除
                </v-btn>
                <div v-if="focusedIndex === index">
                    <div class="title">
                        <h4>結合層 (Dense)</h4>
                    </div>
                    <div class="content">
                        <div>
                            <dt>units</dt>
                            <dd>
                                <input
                                    type="number"
                                    v-model="dense.units"
                                    min="32"
                                    step="32"
                                    max="1024"
                                />
                                <input
                                    type="checkbox"
                                    id="class_length"
                                    v-model="dense.isUsingClassLength"
                                    :style="'margin-left: 1.5em;'"
                                />
                                <label for="class_length">
                                    データセットのフォルダ数を使用
                                </label>
                            </dd>
                        </div>
                        <div>
                            <dt>activation</dt>
                            <dd>
                                <select v-model="dense.activation">
                                    <option
                                        v-for="activation in activations"
                                        :key="activation"
                                    >
                                        {{ activation }}
                                    </option>
                                </select>
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
            @click="addDense"
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
        @click="doneDenseSettings()"
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
        @click="editDenseSettings()"
        v-else
    >
        <template v-slot:prepend>
            <v-icon left>mdi-square-edit-outline</v-icon>
        </template>
        編集
    </v-btn>
</template>
