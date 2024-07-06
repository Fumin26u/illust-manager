import { ref } from 'vue'
import { defineStore } from 'pinia'
import { PixSearch } from '@/types'

export const usePixivStore = defineStore('pixiv', () => {
    const searchQuery = ref<PixSearch>({
        userID: 13936467,
        tag: '',
        getPostType: 'bookmark',
        getNumberOfPost: '200',
        minBookmarks: 2000,
        isGetFromPreviousPost: true,
        includeTags: false,
        suspendID: '',
        isIgnoreSensitive: false,
    })

    return { searchQuery }
})