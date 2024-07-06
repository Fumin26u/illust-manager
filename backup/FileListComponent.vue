<script setup lang="ts">
import { ref, onMounted } from 'vue'
import ApiManager from '@/server/apiManager'
import { apiPath } from '@/assets/ts/paths'

const props = defineProps(['title', 'type'])
const emits = defineEmits(['setSelectedFile'])

const files = ref<string[]>([])
const selected = ref<string>('')

// APIを介して訓練モデル、画像フォルダ一覧を取得
const apiManager = new ApiManager()
const getFiles = async () => {
    const response = await apiManager.get(`${apiPath}/evaluate/${props.type}`)
    files.value = response.content.data
    selected.value = files.value[0]
}

const fileSelect = () => {
    emits('setSelectedFile', props.type, selected.value)
}

onMounted(async () => {
    await getFiles()
    fileSelect()
})
</script>

<template>
    <div>
        <dt>{{ title }}</dt>
        <dd>
            <select v-model="selected" @change="fileSelect">
                <option v-for="(file, index) in files" :key="index">
                    {{ file }}
                </option>
            </select>
        </dd>
    </div>
</template>
