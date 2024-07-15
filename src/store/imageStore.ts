import { ref } from 'vue'
import { defineStore } from 'pinia'
import { RawImage, Image, ImageTag } from '@/types/image'
import { formatCurrentTime, formatUnixTime } from '@/assets/ts/formatDate'
import { apiOrigin } from '@/assets/ts/paths'

export const useImageStore = defineStore('image', () => {
    const rawImages = ref<RawImage[]>([])
    const images = ref<Image[]>([])

    const getRawImageInfo = (file: File) => {
        const imageInfo = ref<RawImage>({
            name: '',
            path: '',
            tags: [],
        })
        imageInfo.value.created_at = file.lastModified
            ? formatUnixTime(file.lastModified)
            : formatCurrentTime()
        imageInfo.value.updated_at = imageInfo.value.created_at
        imageInfo.value.name = file.name
        imageInfo.value.path = URL.createObjectURL(file)

        rawImages.value.push(imageInfo.value)
    }

    const loadImages = (images: RawImage[]) => {
        rawImages.value = images.map((image: RawImage) => {
            return {
                path: `${apiOrigin}/${image.path}`,
                name: image.name,
                platform: image.platform,
                directory: image.directory,
            }
        })
    }

    const insertImportedPaths = (imported_paths: string[]) => {
        rawImages.value.forEach((image, index) => {
            image.imported_path = imported_paths[index]
        })
    }
    return {
        rawImages,
        images,
        getRawImageInfo,
        loadImages,
        insertImportedPaths,
    }
})
