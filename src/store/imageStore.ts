import { ref } from 'vue'
import { defineStore } from 'pinia'
import { Image, ImageTag } from '@/types/image'
import { formatCurrentTime, formatUnixTime } from '@/assets/ts/formatDate'
import { apiOrigin } from '@/assets/ts/paths'

export const useImageStore = defineStore('image', () => {
    const images = ref<Image[]>([])

    const getImageInfo = (file: File) => {
        const imageInfo = ref<Image>({
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

        images.value.push(imageInfo.value)
    }

    const loadImages = (rawImages: Image[]) => {
        images.value = rawImages.map((rawImage: Image) => {
            return {
                path: `${apiOrigin}/${rawImage.path}`,
                name: rawImage.name,
                platform: rawImage.platform,
                directory: rawImage.directory,
            }
        })
        console.log(images.value)
    }

    const insertImportedPaths = (imported_paths: string[]) => {
        images.value.forEach((image, index) => {
            image.imported_path = imported_paths[index]
        })
    }

    const insertImages = (taggedImages: Image[]) => {
        const map = new Map<string, Image>()
        images.value.forEach((image) => {
            map.set(image.name, image)
        })

        taggedImages.forEach((taggedImage) => {
            if (map.has(taggedImage.name)) {
                map.set(taggedImage.name, {
                    ...map.get(taggedImage.name),
                    ...taggedImage,
                })
            } else {
                map.set(taggedImage.name, taggedImage)
            }
        })
        images.value = Array.from(map.values())
        console.log(images.value)
    }

    return {
        images,
        getImageInfo,
        loadImages,
        insertImportedPaths,
        insertImages,
    }
})
