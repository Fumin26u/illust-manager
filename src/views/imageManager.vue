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
const rawImages = computed(() => imageStore.rawImages)
const taggedImages = computed(() => imageStore.images)

const endPoint = createEndPoint(`/api`)
const platform = 'local'
const isImported = ref<boolean>(true)
const isTagged = ref<boolean>(false)
const selectedIndex = ref<number>(-1)
const selectedRawImage = computed(() => {
    if (rawImages.value.length === 0) return null
    return rawImages.value[selectedIndex.value]
})
const selectedTaggedImage = computed(() => {
    if (taggedImages.value.length === 0) return null
    return taggedImages.value[selectedIndex.value]
})

const switchIsImported = (flag: boolean) => {
    isImported.value = flag
}

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
        selectedIndex.value = 0
        switchIsImported(true)
    } catch (error) {
        console.error(error)
    }
}

const importImageToApp = async () => {
    const importImages = await Promise.all(
        rawImages.value.map(async (rawImage) => {
            return {
                base64: await convertImageToBase64(rawImage.path),
                ...rawImage,
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

        await updateCounter(rawImages.value.length)
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
    try {
        const response = await axios.post(`${endPoint}/image/tag/generate`, {
            images: rawImages.value,
        })

        if (response.status !== 200) {
            throw new Error('タグの生成に失敗しました')
        }

        imageStore.insertImages(response.data.content)
        isTagged.value = true
    } catch (error) {
        console.error(error)
    }
}

// 画像にタグを付与して保存
const saveTagsInImage = async () => {
    console.log(taggedImages.value)
}
</script>
<template>
    <HeaderComponent />
    <main class="main-container" id="page-image-manager">
        <section class="section-import-image">
            <ImportImage @switchIsImported="switchIsImported" />
            <ImportedImageList :platform="platform" @loadImage="loadImage" />
        </section>
        <section class="section-image-list" v-if="rawImages.length !== 0">
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
            <div class="image-management">
                <dl class="image-list">
                    <div v-for="(rawImage, index) in rawImages" :key="index">
                        <dt>{{ rawImage.name }}</dt>
                        <dd @click="selectedIndex = index">
                            <img
                                :src="
                                    rawImage.imported_path !== undefined
                                        ? rawImage.imported_path
                                        : rawImage.path
                                "
                                :alt="rawImage.name"
                            />
                        </dd>
                    </div>
                </dl>
                <ul class="image-detail">
                    <div class="no-image" v-if="selectedRawImage === null">
                        <p>画像が選択されていません</p>
                    </div>
                    <div v-else>
                        <li class="filename">
                            <p>{{ selectedRawImage.name }}</p>
                        </li>
                        <li class="image">
                            <img
                                :src="
                                    selectedRawImage.imported_path !== undefined
                                        ? selectedRawImage.imported_path
                                        : selectedRawImage.path
                                "
                                :alt="selectedRawImage.name"
                            />
                        </li>
                    </div>
                    <div v-if="selectedTaggedImage !== null">
                        <li class="tags">
                            <div
                                v-for="(
                                    tag, tagIndex
                                ) in selectedTaggedImage.tags"
                                :key="tagIndex"
                            >
                                <input
                                    :id="tag.name_en"
                                    type="checkbox"
                                    v-model="tag.is_saved"
                                />
                                <label :for="tag.name_en">
                                    {{ tag.name_en }} (信頼度:
                                    {{ tag.confidence }})
                                </label>
                            </div>
                        </li>
                    </div>
                    <ButtonComponent
                        v-if="selectedTaggedImage !== null"
                        @click="saveTagsInImage()"
                        text="タグを付与して保存"
                        :buttonClass="'btn-common blue'"
                    />
                </ul>
            </div>
        </section>
    </main>
</template>
