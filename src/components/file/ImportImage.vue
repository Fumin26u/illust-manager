<script setup lang="ts">
import { useImageStore } from '@/store/imageStore'

const imageStore = useImageStore()

const importImage = (event: Event) => {
    const input = event.target as HTMLInputElement
    imageStore.rawImages = []
    if (input.files) {
        const files = Array.from(input.files)
        files.forEach((file) => {
            imageStore.getRawImageInfo(file)
        })
    }
}
</script>

<template>
    <div>
        <h2>画像のインポート</h2>
        <div>
            <input type="file" webkitdirectory @change="importImage" />
        </div>
    </div>
</template>
