<script setup lang="ts">
import { ref } from 'vue'
import ApiManager from '@/server/apiManager'
import { apiPath } from '@/assets/ts/paths'

const directoryPath = ref<File | null>(null)

const apiManager = new ApiManager()
const getDirectory = async (event: Event) => {
    const input = event.target as HTMLInputElement
    const files = input.files

    if (files && files.length > 0) {
        const formData = new FormData()
        formData.append('directoryPath', files[0])

        try {
            const response = apiManager.get(`${apiPath}/directory/`, formData)
            console.log(response)
        } catch (error) {
            console.error(error)
        }
    }
}
</script>

<template>
    <section id="page-evaluate">
        <div class="title-area">
            <h1 class="title">画像の評価</h1>
        </div>
        <div class="reference-form">
            <input type="file" webkitdirectory @change="getDirectory" />
            <p v-if="directoryPath !== null">{{ directoryPath }}</p>
        </div>
    </section>
</template>
