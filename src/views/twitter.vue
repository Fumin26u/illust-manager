<script setup lang="ts">
import HeaderComponent from '@/components/HeaderComponent.vue'
import ButtonComponent from '@/components/ButtonComponent.vue'

import { ref, onMounted } from 'vue'
import ApiManager from '@/server/apiManager'
import { TweetInfo, TweetImage, TwiSearch } from '@/types'
import { apiPath } from '@/assets/ts/paths'

import '@/assets/scss/imagedler/twiForm.scss'

const errorMessage = ref<string>('')
const search = ref<TwiSearch>({
    twitterID: '',
    getTweetType: 'liked_tweets',
    getNumberOfTweet: '150',
    isGetFromPreviousTweet: true,
    suspendID: '',
})

// 入力フォームのバリデーション
const inputValidation = (): string => {
    let error = ''
    if (search.value.twitterID === '') {
        error = 'Twitter IDが入力されていません。'
    }

    const numTweet = parseInt(search.value.getNumberOfTweet)
    if (isNaN(numTweet)) {
        error = '取得ツイート数は数値で入力してください。'
    }
    if (numTweet < 5 || numTweet > 3000) {
        error = '取得できるツイートの最小値は10, 最大値は3000です。'
    }
    return error
}

// twitterユーザーID・中断IDを取得
const apiManager = new ApiManager()
const getUserInfo = async () => {
    const response = await apiManager.get(`${apiPath}/api/getTwitterInfo`)
    return response.content
}

// APIから画像付きツイートを取得
const tweetInfo = ref<TweetInfo[]>([])
const isLoadImages = ref<boolean>(false)
const getTweet = async () => {
    isLoadImages.value = true
    // 入力フォームのバリデーションを行いエラーがある場合は中断
    errorMessage.value = inputValidation()
    if (errorMessage.value !== '') return

    const response = await apiManager.post(`${apiPath}/twitter/getImages`, {
        content: search.value,
    })
    // それぞれの画像にDL可否判定の値を追加
    tweetInfo.value = response.map((tweet: TweetInfo) => {
        return {
            postID: tweet.postID,
            post_time: tweet.post_time,
            user: tweet.user,
            text: tweet.text,
            url: tweet.url,
            images: tweet.images.map((image: TweetImage, index: number) => {
                return {
                    id: `${tweet.postID}_${index}`,
                    url: image,
                    selected: true,
                }
            }),
        }
    })
    isLoadImages.value = false
}

// 画像のダウンロード
const getSelectedImagesFromTweets = (tweets: TweetInfo[]) => {
    const images: string[] = []
    tweets.map((tweet) => {
        tweet.images.map((image) => {
            if (image.selected) images.push(image.url)
        })
    })

    return images
}

const dlImage = async () => {
    isLoadImages.value = true
    // 選択した画像一覧の配列を作成
    const imagePaths = getSelectedImagesFromTweets(tweetInfo.value)
    // 画像URL一覧をAPIに送り画像をDL
    const downloadResponse = await apiManager.post(
        `${apiPath}/twitter/downloadImages`,
        {
            content: imagePaths,
        }
    )

    // 画像のDLとzipファイルの作成に成功した場合、zipをDLする
    if (downloadResponse.error) {
        errorMessage.value = downloadResponse.content
        return
    }

    const link = document.createElement('a')
    link.href = `${apiPath}/twitter/getZip`
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)

    // APIを叩いて保存回数と画像保存枚数、最新取得画像を更新
    await apiManager.post(`${apiPath}/api/updateTwitterInfo`, {
        imageCount: imagePaths.length,
        latestID: tweetInfo.value[0].postID,
        twitterID: search.value.twitterID,
    })
    isLoadImages.value = false
}

onMounted(async () => {
    const userInfo = await getUserInfo()
    search.value.twitterID = userInfo[0]['id']
    search.value.suspendID = userInfo[0]['post']
})
</script>
<template>
    <HeaderComponent />
    <main class="main-container twi-template">
        <section class="common-form">
            <dl class="form-box">
                <div>
                    <dt>
                        Twitter ID
                        <em>*</em>
                    </dt>
                    <dd><input v-model="search.twitterID" type="text" /></dd>
                </div>
                <div>
                    <dt>
                        取得内容
                        <em>*</em>
                    </dt>
                    <dd class="radio-list">
                        <div>
                            <input
                                id="get-like"
                                v-model="search.getTweetType"
                                type="radio"
                                value="liked_tweets"
                            />
                            <label for="get-like">いいね</label>
                        </div>
                        <div>
                            <input
                                id="get-tweet"
                                v-model="search.getTweetType"
                                type="radio"
                                value="tweets"
                                disabled
                            />
                            <label for="get-tweet">ツイート</label>
                        </div>
                        <div>
                            <input
                                id="get-bookmark"
                                v-model="search.getTweetType"
                                type="radio"
                                value="bookmarks"
                                disabled
                            />
                            <label for="get-bookmark">ブックマーク</label>
                        </div>
                    </dd>
                </div>
                <div>
                    <dt>
                        取得ツイート数
                        <em>*</em>
                        <br />
                        (最大300)
                    </dt>
                    <dd>
                        <input
                            v-model="search.getNumberOfTweet"
                            type="number"
                            min="5"
                            max="1000"
                            step="5"
                        />
                    </dd>
                </div>
                <div>
                    <dt>取得を中断するID</dt>
                    <dd>
                        <input
                            type="number"
                            id="suspend-id"
                            v-model="search.suspendID"
                        />
                    </dd>
                </div>
                <div>
                    <dt>詳細設定</dt>
                    <dd>
                        <input
                            id="get-pre"
                            v-model="search.isGetFromPreviousTweet"
                            type="checkbox"
                        />
                        <label for="get-pre">前回DLした画像以降を取得</label>
                    </dd>
                </div>
                <div v-show="isLoadImages" class="btn-cover"></div>
                <ButtonComponent
                    @click="getTweet()"
                    text="ツイートを取得"
                    :buttonClass="'btn-common green'"
                />
            </dl>
        </section>
        <p>{{ errorMessage }}</p>
        <section v-if="tweetInfo.length > 0" class="tweet-list post-list">
            <div v-show="isLoadImages" class="btn-cover"></div>
            <div class="title-area">
                <h2>取得ツイート一覧</h2>
                <p v-if="tweetInfo.length > 0" class="caption">
                    取得ツイート数: {{ tweetInfo.length }}
                </p>
            </div>
            <div class="dl-image-area">
                <ButtonComponent
                    @click="dlImage()"
                    text="ダウンロード"
                    :buttonClass="'btn-common green'"
                />
                <p class="caption">※選択している画像をDLします。</p>
            </div>
            <div
                v-for="tweet in tweetInfo"
                :key="tweet.postID"
                class="post-info"
            >
                <h3 class="user-name">{{ tweet.user }}</h3>
                <p class="tweet-text">{{ tweet.text }}</p>
                <div
                    v-for="image in tweet.images"
                    :key="image.id"
                    class="tweet-image"
                >
                    <input
                        :id="image.id"
                        v-model="image.selected"
                        type="checkbox"
                    />
                    <label
                        :for="image.id"
                        :class="!image.selected ? 'not-selected' : ''"
                    >
                        <img :src="image.url" :alt="tweet.text" />
                    </label>
                </div>
                <div class="post-url">
                    <a :href="tweet.url">ツイート元リンク</a>
                </div>
            </div>
        </section>
    </main>
</template>
