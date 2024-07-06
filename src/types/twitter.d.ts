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
