<script setup lang="ts">
import HeaderComponent from '@/components/HeaderComponent.vue'
import ImportImage from '@/components/file/ImportImage.vue'
import ImportedImageList from '@/components/file/ImportedImageList.vue'
import VImage from '@/components/file/VImage.vue'

import axios from '@/axios'
import { ref, computed } from 'vue'
import { createEndPoint } from '@/assets/ts/paths'
import { useImageStore } from '@/store/imageStore'
import { useTagStore } from '@/store/tagStore'
import { convertImageToBase64 } from '@/assets/ts/base64'

import '@/assets/scss/imageManager/main.scss'

const imageStore = useImageStore()
const images = computed(() => imageStore.images)
const tagStore = useTagStore()
const tags = computed(() => tagStore.tags)

type Platform = 'local' | 'twitter' | 'pixiv'
const endPoint = createEndPoint(`/api`)
const platform = ref<Platform>('local')
const isImported = ref<boolean>(true)
const isTagged = ref<boolean>(false)
const importTabs = ref<string>('local')

const selectedIndex = ref<number>(0)
const selectIndex = (index: number) => (selectedIndex.value = index)

const switchPlatform = (pf: Platform) => {
    platform.value = pf
}

const selectedImage = computed(() => {
    if (images.value.length === 0) return null
    return images.value[selectedIndex.value]
})

const switchIsImported = (flag: boolean) => {
    isImported.value = flag
}

const loadImage = async (directoryName: string) => {
    try {
        const response = await axios.post(`${endPoint}/image/load`, {
            platform: platform.value,
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
        imageStore.insertImportedPaths(
            response.data.imported_paths,
            platform.value
        )
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
            images: images.value,
        })

        if (response.status !== 200) {
            throw new Error('タグの生成に失敗しました')
        }

        imageStore.insertImages(response.data.content)
        tagStore.getTagsByCategory(1)
        isTagged.value = true
    } catch (error) {
        console.error(error)
    }
}

// 画像にタグを追加
const selectedTagId = ref<number>(0)
const addTag = () => {
    const tag = tags.value.find((tag) => tag.id === selectedTagId.value)
    if (tag === undefined) return
    imageStore.addTag(selectedIndex.value, tag)
}

// 画像にタグを付与して保存
const saveTagsInImage = async () => {
    try {
        const response = await axios.post(`${endPoint}/image/save`, {
            images: images.value,
        })

        if (response.status !== 200) {
            throw new Error('タグの保存に失敗しました')
        }
    } catch (error) {
        console.error(error)
    }
}
</script>
<template>
    <HeaderComponent />
    <main class="main-container" id="page-image-manager">
        <section class="section-import-image">
            <h2>画像のインポート</h2>
            <v-card class="v-card-import-image">
                <v-tabs v-model="importTabs" bg-color="secondary">
                    <v-tab value="local">ローカル</v-tab>
                    <v-tab value="app">アプリ内</v-tab>
                </v-tabs>

                <v-card-text>
                    <v-tabs-window v-model="importTabs">
                        <v-tabs-window-item value="local">
                            <ImportImage @switchIsImported="switchIsImported" />
                        </v-tabs-window-item>
                        <v-tabs-window-item value="app">
                            <ImportedImageList
                                @loadImage="loadImage"
                                @switch-platform="switchPlatform"
                            />
                        </v-tabs-window-item>
                    </v-tabs-window>
                </v-card-text>
            </v-card>
        </section>
        <section class="section-image-list" v-if="images.length !== 0">
            <h2>画像一覧</h2>
            <v-btn
                v-if="!isImported"
                @click="importImageToApp()"
                color="secondary"
            >
                インポート
            </v-btn>
            <v-btn v-else @click="generateTagsFromImage()" color="primary">
                タグ生成
            </v-btn>
            <div class="image-management">
                <dl class="image-list">
                    <VImage
                        v-for="(image, index) in images"
                        :key="index"
                        :image="image"
                        :index="index"
                        @select="selectIndex"
                    />
                </dl>
                <ul class="image-detail">
                    <div class="no-image" v-if="selectedImage === null">
                        <p>画像が選択されていません</p>
                    </div>
                    <div class="image-card" v-else>
                        <v-card>
                            <v-img
                                class="bg-grey-lighten-3 img-content"
                                max-height="400"
                                :src="
                                    selectedImage.imported_path !== undefined
                                        ? selectedImage.imported_path
                                        : selectedImage.path
                                "
                                :alt="selectedImage.name"
                                cover
                            ></v-img>
                            <v-card-title class="img-text">
                                {{ selectedImage.name }}
                            </v-card-title>
                        </v-card>
                    </div>
                    <div class="add-tag">
                        <v-autocomplete
                            label="タグを選択"
                            class="tag-selector"
                            :items="tags"
                            item-value="id"
                            item-title="name_en"
                            variant="underlined"
                            v-model="selectedTagId"
                        ></v-autocomplete>
                        <v-btn
                            @click="addTag"
                            color="secondary"
                            class="btn-add-tag"
                        >
                            追加
                        </v-btn>
                    </div>
                    <div class="tag-list" v-if="selectedImage !== null">
                        <li class="tags">
                            <div
                                v-for="(tag, tagIndex) in selectedImage.tags"
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
                    <v-btn
                        v-if="selectedImage !== null"
                        @click="saveTagsInImage()"
                        color="primary"
                    >
                        保存
                    </v-btn>
                </ul>
            </div>
        </section>
    </main>
</template>
