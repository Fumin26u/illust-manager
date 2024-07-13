import { ref } from 'vue'
import { defineStore } from 'pinia'
import { PixivSearch, TwitterSearch } from '@/types/search'
import type { Search } from '@/types/search'

export const useSearchStore = defineStore('search', () => {
    const pixivSearch = ref<PixivSearch>({
        id: 0,
        tag: '',
        type: 'bookmark',
        getNumberOfPost: 200,
        minBookmarks: 2000,
        isGetFromPreviousPost: true,
        includeTags: false,
        isIgnoreSensitive: false,
    })

    const twitterSearch = ref<TwitterSearch>({
        id: '',
        type: 'liked_tweets',
        getNumberOfPost: 200,
        isGetFromPreviousPost: true,
    })

    const search = ref<Search>(twitterSearch.value)

    const switchSearchPlatform = (platform: string) => {
        switch (platform) {
            case 'pixiv':
                search.value = pixivSearch.value
                break
            case 'twitter':
                search.value = twitterSearch.value
                break
            default:
                search.value = twitterSearch.value
        }
    }

    return { search, twitterSearch, pixivSearch, switchSearchPlatform }
})
