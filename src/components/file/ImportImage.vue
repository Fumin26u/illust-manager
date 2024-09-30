<script setup lang="ts">
import { useImageStore } from '@/store/imageStore'
import { defineEmits } from 'vue'

const emit = defineEmits(['switchIsImported'])
const imageStore = useImageStore()

const importImage = (event: Event) => {
    const input = event.target as HTMLInputElement
    imageStore.images = []
    if (input.files) {
        const files = Array.from(input.files)
        files.forEach((file) => {
            imageStore.getImageInfo(file)
        })
    }
    emit('switchIsImported', false)
}
</script>

<template>
    <div>
        <v-file-input
            type="file"
            variant="solo-inverted"
            label="フォルダを選択"
            webkitdirectory
            @change="importImage"
        />
    </div>
</template>
