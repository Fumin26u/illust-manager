<script setup lang="ts">
import ButtonComponent from '@/components/ButtonComponent.vue'

import { ref, computed, defineEmits } from 'vue'
import axios from '@/axios'
import { createEndPoint } from '@/assets/ts/paths'
import { Directory } from '@/types/image'

const props = defineProps<{
    platform: string
}>()
const emits = defineEmits(['loadImage'])

const endPoint = createEndPoint(`/api/image`)
const directories = ref<Directory[]>([])
const selectedDirectory = ref<string>('')
const fileCount = computed(() => {
    const directory = directories.value.find(
        (directory) => directory.name === selectedDirectory.value
    )
    return directory ? directory.count : 0
})

const getDirectories = async () => {
    try {
        const response = await axios.get(
            `${endPoint}/directories?platform=${props.platform}`
        )
        if (response.status !== 200) {
            throw new Error('ディレクトリ情報の取得に失敗しました')
        }
        directories.value = response.data.directories
        selectedDirectory.value = directories.value[0].name
    } catch (error) {
        console.error(error)
    }
}
getDirectories()

const loadImage = () => {
    emits('loadImage', selectedDirectory.value)
}
</script>

<template>
    <div>
        <h2>インポート済みの画像フォルダを選択</h2>
        <div>
            <select v-model="selectedDirectory">
                <option v-for="(directory, index) in directories" :key="index">
                    {{ directory.name }}
                </option>
            </select>
            <span v-if="selectedDirectory !== ''">
                (ファイル数: {{ fileCount }})
            </span>
        </div>
        <ButtonComponent
            @click="loadImage"
            text="画像を読み込む"
            :buttonClass="'btn-small green'"
        />
    </div>
</template>
