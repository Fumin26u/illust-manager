<script setup lang="ts">
import HeaderComponent from '@/components/HeaderComponent.vue'
import ButtonComponent from '@/components/ButtonComponent.vue'

import axios from 'axios'
import { createEndPoint } from '@/assets/ts/paths'
import { ref } from 'vue'
import { Tweet, TweetImage, Search } from '@/types/twitter'

import '@/assets/scss/twiForm.scss'

const errorMessage = ref<string>('')
const search = ref<Search>({
    twitterID: '',
    getTweetType: 'liked_tweets',
    getNumberOfTweet: '150',
    isGetFromPreviousTweet: true,
})

const endPoint = createEndPoint('/api/twitter')
const userId = localStorage.getItem('user_id')

// twitter IDを取得
const getTwitterID = async () => {
    try {
        const response = await axios.get(
            `${endPoint}/${localStorage.getItem('user_id')}`
        )
        if (response.status !== 200) {
            throw new Error('Twitter IDの取得に失敗しました')
        }
        search.value.twitterID = response.data.platform_id
    } catch (error) {
        console.error(error)
    }
}
getTwitterID()

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

// APIから画像付きツイートを取得
const tweets = ref<Tweet[]>([])
const isLoadImages = ref<boolean>(false)
const getTweet = async () => {
    isLoadImages.value = true
    // 入力フォームのバリデーションを行いエラーがある場合は中断
    errorMessage.value = inputValidation()
    if (errorMessage.value !== '') return

    try {
        const response = await axios.post(
            `${endPoint}/getTweet/${userId}`,
            search.value
        )

        if (response.status !== 200) {
            throw new Error('Tweet情報の取得に失敗しました')
        }

        tweets.value = response.data.map((tweet: Tweet) => {
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
    } catch (error) {
        console.error(error)
    }
}

const dlImage = async () => {
    isLoadImages.value = true

    // 画像URL一覧をAPIに送り画像をDL
    const response = await axios.post(`${endPoint}/download/${userId}`, {
        tweet: tweets.value,
    })

    if (response.status !== 200) {
        throw new Error('画像情報の取得に失敗しました')
    }

    const link = document.createElement('a')
    link.href = `${endPoint}/downloadZip?timestamp=${response.data.now_time}`
    link.target = '_blank'
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
}
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
        <section v-if="tweets.length > 0" class="tweet-list post-list">
            <div v-show="isLoadImages" class="btn-cover"></div>
            <div class="title-area">
                <h2>取得ツイート一覧</h2>
                <p v-if="tweets.length > 0" class="caption">
                    取得ツイート数: {{ tweets.length }}
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
            <div v-for="tweet in tweets" :key="tweet.postID" class="post-info">
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
