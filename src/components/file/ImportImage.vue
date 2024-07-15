<script setup lang="ts">
import { ref } from 'vue'
import { useImageStore } from '@/store/imageStore'

const imageStore = useImageStore()

const importImage = (event: Event) => {
    const input = event.target as HTMLInputElement
    if (input.files) {
        const files = Array.from(input.files)
        files.forEach((file) => {
            imageStore.getRawImageInfo(file)
        })
        console.log(imageStore.rawImages)
    }
}
</script>

<template>
    <div>
        <dd>
            <input type="file" webkitdirectory @change="importImage" />
        </dd>
    </div>
</template>
