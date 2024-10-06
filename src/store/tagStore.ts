import { ref } from 'vue'
import { defineStore } from 'pinia'
import { Tag, Category, CategoryMaster } from '@/types/tag'
import { createEndPoint } from '@/assets/ts/paths'
import { get, put } from '@/api'

export const useTagStore = defineStore('tag', () => {
    const tags = ref<Tag[]>([])
    const categories = ref<Category[]>([])
    const endPoint = createEndPoint('/api')

    const getTags = async () => (tags.value = await get(`${endPoint}/tag`))

    const getTagsByCategory = async (categoryId: number) =>
        (tags.value = await get(
            `${endPoint}/tag/category?category_id=${categoryId}`
        ))

    const getCategories = async () =>
        (categories.value = await get(`${endPoint}/category`))

    const search = async (query: string) =>
        (tags.value = await get(`${endPoint}/tag/search?query=${query}`))

    const updateTag = async (tag: Tag) => {
        const updatedTag = await put(`${endPoint}/tag/update`, tag)
        const index = tags.value.findIndex((t) => t.id === updatedTag.id)
        tags.value[index] = updatedTag
    }

    const updateTagCategoryIds = async (
        targetTags: Tag[],
        categoryId: number
    ) => {
        const updatedTags = await put(`${endPoint}/tag/update/cluster`, {
            tags: targetTags,
            category_id: categoryId,
        })

        updatedTags.forEach((updatedTag: Tag) => {
            const index = tags.value.findIndex(
                (tag) => tag.id === updatedTag.id
            )
            tags.value[index] = updatedTag
        })
    }

    return {
        tags,
        categories,
        getTags,
        getTagsByCategory,
        getCategories,
        search,
        updateTag,
        updateTagCategoryIds,
    }
})
