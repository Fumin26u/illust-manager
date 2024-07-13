export interface PixSearch {
    userID: number
    tag: string
    getPostType: 'bookmark' | 'post' | 'tag'
    getNumberOfPost: string
    minBookmarks: number
    isGetFromPreviousPost: boolean
    includeTags: boolean
    isIgnoreSensitive: boolean
}

export interface PixivPost {
    postID: string
    post_time: boolean
    user: string
    text: string
    images: PixivPostImage[]
    url: string
}

export interface PixivPostImage {
    id: string
    url: string
    selected: boolean
}
