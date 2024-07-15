<script setup lang="ts">
import HeaderComponent from '@/components/HeaderComponent.vue'
import ButtonComponent from '@/components/ButtonComponent.vue'
import GetLocalImage from '@/components/file/ImportImage.vue'

import axios from '@/axios'
import { ref, computed } from 'vue'
import { createEndPoint } from '@/assets/ts/paths'
import { useSearchStore } from '@/store/searchStore'
import { useImageStore } from '@/store/imageStore'

import '@/assets/scss/imageManager/main.scss'

const imageStore = useImageStore()
const images = computed(() => imageStore.rawImages)
</script>
<template>
    <HeaderComponent />
    <main class="main-container" id="page-image-manager">
        <section class="section-import-image">
            <h2>画像のインポート</h2>
            <GetLocalImage />
        </section>
        <section class="section-image-list" v-if="images.length !== 0">
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
