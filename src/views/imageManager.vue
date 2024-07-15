<script setup lang="ts">
import HeaderComponent from '@/components/HeaderComponent.vue'
import ButtonComponent from '@/components/ButtonComponent.vue'
import ImportImage from '@/components/file/ImportImage.vue'
import ImportedImageList from '@/components/file/ImportedImageList.vue'

import axios from '@/axios'
import { ref, computed } from 'vue'
import { createEndPoint } from '@/assets/ts/paths'
import { useImageStore } from '@/store/imageStore'
import { convertImageToBase64 } from '@/assets/ts/base64'

import '@/assets/scss/imageManager/main.scss'

const imageStore = useImageStore()
const images = computed(() => imageStore.rawImages)

const endPoint = createEndPoint(`/api`)
const platform = 'local'
const isImported = ref<boolean>(false)

const loadImage = async (directoryName: string) => {
    try {
        const response = await axios.post(`${endPoint}/image/load`, {
            platform: platform,
            directory_name: directoryName,
        })
        if (response.status !== 200) {
            throw new Error('画像の取得に失敗しました')
        }

        imageStore.loadImages(response.data.images)
        isImported.value = true
    } catch (error) {
        console.error(error)
    }
}

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
        isImported.value = true
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

// 画像からタグを生成
const generateTagsFromImage = async () => {
    console.log(images.value)
    try {
        const response = await axios.post(`${endPoint}/image/tag/generate`, {
            images: images.value,
        })
    } catch (error) {
        console.error(error)
    }
}
</script>
<template>
    <HeaderComponent />
    <main class="main-container" id="page-image-manager">
        <section class="section-import-image">
            <ImportImage />
            <ImportedImageList :platform="platform" @loadImage="loadImage" />
        </section>
        <section class="section-image-list" v-if="images.length !== 0">
            <h2>画像一覧</h2>
            <ButtonComponent
                v-if="!isImported"
                @click="importImageToApp()"
                text="アプリにインポート"
                :buttonClass="'btn-common green'"
            />
            <ButtonComponent
                v-else
                @click="generateTagsFromImage()"
                text="タグを生成"
                :buttonClass="'btn-common blue'"
            />
            <dl class="image-list">
                <div v-for="(image, index) in images" :key="index">
                    <dt>{{ image.name }}</dt>
                    <dd>
                        <img
                            :src="
                                image.imported_path !== undefined
                                    ? image.imported_path
                                    : image.path
                            "
                            :alt="image.name"
                        />
                    </dd>
                </div>
            </dl>
        </section>
    </main>
</template>
