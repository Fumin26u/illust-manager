import { ref } from 'vue'
import { PixSearch, TwiSearch } from '@/types'

export const pixUserData = ref<PixSearch>({
    userID: 13936467,
    getPostType: 'bookmark',
    getNumberOfPost: '150',
    isGetFromPreviousPost: true,
    includeTags: false,
    suspendID: '',
})

export const twiUserData = ref<TwiSearch>({
    twitterID: 'fumin_ci',
    getTweetType: 'liked_tweets',
    getNumberOfTweet: '150',
    isGetFromPreviousTweet: true,
})
