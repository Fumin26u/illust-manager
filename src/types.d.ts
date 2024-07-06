/* -----------------  

    アカウント関連

----------------- */
export interface UserInfo {
    id: number
    email: string
    user_name: string
    uuid: string
    created_at: string
    updated_at: string
}

export interface UserPixivInfo {
    id: string
    post: string
    tag: string
}

export interface UserTwitterInfo {
    id: string
    post: string
}

/* -----------------  

    ImageDLer

----------------- */
// Twitter
export interface TwiSearch {
    twitterID: string
    getTweetType: 'liked_tweets' | 'tweets' | 'bookmarks'
    getNumberOfTweet: string
    isGetFromPreviousTweet: boolean
    suspendID: string
}

export interface TweetImage {
    id: string
    url: string
    selected: boolean
}

export interface TweetInfo {
    postID: string
    post_time: boolean
    user: string
    text: string
    images: TweetImage[]
    url: string
}

// pixiv
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
