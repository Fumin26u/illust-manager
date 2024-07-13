export interface PixivSearch {
    id: number
    tag: string
    type: 'bookmark' | 'post' | 'tag'
    getNumberOfPost: number
    minBookmarks: number
    isGetFromPreviousPost: boolean
    includeTags: boolean
    isIgnoreSensitive: boolean
}

export interface TwitterSearch {
    id: string
    type: 'liked_tweets' | 'tweets' | 'bookmark'
    getNumberOfPost: number
    isGetFromPreviousPost: boolean
}

export type Search = PixivSearch | TwitterSearch
