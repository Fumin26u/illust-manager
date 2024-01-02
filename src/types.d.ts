export interface EvaluatedResult {
    className: string
    probability: string
}

export interface ImageInfo {
    rawPath: string
    imagePath: string
    childDir: string
    classList?: EvaluatedResult[]
    className: string
    probability?: string
    isImportant: boolean
    index: number
}

// account関連
export interface UserInfo {
    created_at: string
    updated_at: string
    dl_count: number
    images_count: number
    pixiv: UserPixivInfo[]
    twitter: UserTwitterInfo[]
    twitter_password: string
    user_name: string
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

// Twitter関連
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

// pixiv関連
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
    images: TweetImage[]
    url: string
}

export interface PixPostImage {
    id: string
    url: string
    selected: boolean
}
