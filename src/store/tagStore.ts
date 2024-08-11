import { ref } from 'vue'
import { defineStore } from 'pinia'
import { Tag, Category, CategoryMaster } from '@/types/tag'
import { createEndPoint } from '@/assets/ts/paths'
import axios from '@/axios'

export const useTagStore = defineStore('tag', () => {
    const tags = ref<Tag[]>([])

    const getTags = async (endPoint = createEndPoint('/api/tag')) => {
        try {
            const response = await axios.get(`${endPoint}`)
            if (response.status !== 200) {
                throw new Error('Failed to fetch tags')
            }

            tags.value = response.data
            console.log(tags.value)
        } catch (error) {
            console.error(error)
        }
    }

    const search = async (
        endPoint = createEndPoint('/api/tag/search'),
        query: string
    ) => {
        try {
            const response = await axios.get(`${endPoint}?search=${query}`)
            if (response.status !== 200) {
                throw new Error('Failed to search tags')
            }

            tags.value = response.data
            console.log(tags.value)
        } catch (error) {
            console.error(error)
        }
    }

    return { tags, getTags, search }
})
