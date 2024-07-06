export interface PixSearch {
    userID: number
    tag: string
    getPostType: 'bookmark' | 'post' | 'tag'
    getNumberOfPost: string
    minBookmarks: number
    isGetFromPreviousPost: boolean
    includeTags: boolean
    suspendID: string
    isIgnoreSensitive: boolean
}

export interface PixPostInfo {
    postID: string
    post_time: boolean
    user: string
    text: string
    images: PixPostImage[]
    url: string
}

export interface PixPostImage {
    id: string
    url: string
    selected: boolean
}
