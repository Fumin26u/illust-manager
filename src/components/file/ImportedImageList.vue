<script setup lang="ts">
import ButtonComponent from '@/components/ButtonComponent.vue'

import { ref, computed, watch, defineEmits } from 'vue'
import axios from '@/axios'
import { createEndPoint } from '@/assets/ts/paths'
import { Directory } from '@/types/image'

type Platform = 'local' | 'twitter' | 'pixiv'

const emits = defineEmits(['loadImage', 'switchPlatform'])

const endPoint = createEndPoint(`/api/image`)
const directories = ref<Directory[]>([])
const selectedDirectory = ref<string>('')
const fileCount = computed(() => {
    const directory = directories.value.find(
        (directory) => directory.name === selectedDirectory.value
    )
    return directory ? directory.count : 0
})

const platform = ref<Platform>('local')
watch(platform, () => {
    getDirectories()
    switchPlatform(platform.value)
})

const getDirectories = async () => {
    try {
        const response = await axios.get(
            `${endPoint}/directories?platform=${platform.value}`
        )
        if (response.status !== 200) {
            throw new Error('ディレクトリ情報の取得に失敗しました')
        }
        directories.value = response.data.directories
        selectedDirectory.value =
            directories.value.length > 0 ? directories.value[0].name : ''
    } catch (error) {
        console.error(error)
    }
}
getDirectories()

const loadImage = () => {
    emits('loadImage', selectedDirectory.value)
}

const switchPlatform = (platform: string) => {
    emits('switchPlatform', platform)
}
</script>

<template>
    <div>
        <div>
            <span>プラットフォーム: {{ platform }}</span>
            <v-radio-group v-model="platform" inline>
                <v-radio label="ローカル" value="local"></v-radio>
                <v-radio label="twitter" value="twitter"></v-radio>
                <v-radio label="pixiv" value="pixiv"></v-radio>
            </v-radio-group>
        </div>
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
        <v-btn @click="loadImage" color="secondary" density="comfortable">
            画像を読み込む
        </v-btn>
    </div>
</template>
