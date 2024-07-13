export interface Search {
    twitterID: string
    getTweetType: 'liked_tweets' | 'tweets' | 'bookmarks'
    getNumberOfTweet: string
    isGetFromPreviousTweet: boolean
}

export interface TweetImage {
    id: string
    url: string
    selected: boolean
}

export interface Tweet {
    postID: string
    post_time: boolean
    user: string
    text: string
    images: TweetImage[]
    url: string
}
