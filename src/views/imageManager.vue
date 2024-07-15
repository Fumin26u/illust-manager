<script setup lang="ts">
import HeaderComponent from '@/components/HeaderComponent.vue'
import ButtonComponent from '@/components/ButtonComponent.vue'
import GetLocalImage from '@/components/file/ImportImage.vue'

import axios from '@/axios'
import { ref, computed } from 'vue'
import { createEndPoint } from '@/assets/ts/paths'
import { useImageStore } from '@/store/imageStore'
import { convertImageToBase64 } from '@/assets/ts/base64'

import '@/assets/scss/imageManager/main.scss'

const imageStore = useImageStore()
const images = computed(() => imageStore.rawImages)

const endPoint = createEndPoint(`/api`)

const importImageToApp = async () => {
    const importImages = await Promise.all(
        images.value.map(async (image) => {
            return {
                base64: await convertImageToBase64(image.path),
                ...image,
            }
        })
    )

    try {
        const response = await axios.post(`${endPoint}/download/local/import`, {
            images: importImages,
        })
        if (response.status !== 200) {
            throw new Error('画像のインポートに失敗しました')
        }

        await updateCounter(images.value.length)
        imageStore.insertImportedPaths(response.data.imported_paths)
        console.log(images.value)
    } catch (error) {
        console.error(error)
    }
}

// ダウンロード(?)数の更新
const updateCounter = async (get_images_count: number) => {
    const response = await axios.post(
        `${endPoint}/userPlatformAccount/update`,
        {
            platform: 'local',
            get_images_count: get_images_count,
        }
    )
    return response
}
</script>
<template>
    <HeaderComponent />
    <main class="main-container" id="page-image-manager">
        <section class="section-import-image">
            <h2>画像のインポート</h2>
            <GetLocalImage />
        </section>
        <section class="section-image-list" v-if="images.length !== 0">
            <h2>画像一覧</h2>
            <ButtonComponent
                @click="importImageToApp()"
                text="アプリにインポート"
                :buttonClass="'btn-common green'"
            />
            <dl class="image-list">
                <div v-for="(image, index) in images" :key="index">
                    <dt>{{ image.name }}</dt>
                    <dd>
                        <img :src="image.path" :alt="image.name" />
                    </dd>
                </div>
            </dl>
        </section>
    </main>
</template>
