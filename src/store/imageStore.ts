import { ref } from 'vue'
import { defineStore } from 'pinia'
import { RawImage, Image, ImageTag } from '@/types/image'

export const usePostStore = defineStore('post', () => {
    const rawImages = ref<RawImage[]>([])
    const Images = ref<Image[]>([])
})
