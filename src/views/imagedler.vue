<script setup lang="ts">
import HeaderComponent from '@/components/HeaderComponent.vue'
import ButtonComponent from '@/components/ButtonComponent.vue'
import SearchTwitterForm from '@/components/search/SearchTwitterForm.vue'
import SearchPixivForm from '@/components/search/SearchPixivForm.vue'
import TwitterPost from '@/components/post/TwitterPost.vue'
import PixivPost from '@/components/post/PixivPost.vue'

import axios from 'axios'
import { ref } from 'vue'
import { createEndPoint } from '@/assets/ts/paths'
import { useSearchStore } from '@/store/searchStore'
import { usePostStore } from '@/store/postStore'

const errorMessage = ref<string>('')
const searchStore = useSearchStore()
const postStore = usePostStore()

const platform = ref<string>('twitter')
const endPoint = createEndPoint(`/api`)
const userId = localStorage.getItem('user_id')

const switchPlatform = (pf: string) => {
    searchStore.switchSearchPlatform(pf)
    platform.value = pf
    if (searchStore.search.id === 0) {
        getPlatformID()
    }
}

// pixiv or twitterのuserIDを取得
const getPlatformID = async () => {
    try {
        const response = await axios.get(
            `${endPoint}/${platform.value}/${userId}`
        )
        if (response.status !== 200) {
            throw new Error('Platform IDの取得に失敗しました')
        }
        searchStore.search.id = response.data.platform_id
    } catch (error) {
        console.error(error)
    }
}
getPlatformID()

// 入力フォームのバリデーション
const inputValidation = (): string => {
    let error = ''
    if (searchStore.search.id === null || searchStore.search.id === 0) {
        error = 'ユーザーIDが入力されていません。'
    }

    const numPost = searchStore.search.getNumberOfPost
    if (isNaN(numPost)) {
        error = '取得作品数は数値で入力してください。'
    }
    if (numPost < 1 || numPost > 300) {
        error = '取得できる作品の最小値は1, 最大値は300です。'
    }
    return error
}

const isLoadImages = ref<boolean>(false)
// 画像情報の取得
const getPosts = async () => {
    isLoadImages.value = true
    errorMessage.value = inputValidation()
    if (errorMessage.value !== '') return

    try {
        const response = await axios.post(
            `${endPoint}/${platform.value}/getPost/${userId}`,
            searchStore.search
        )

        if (response.status !== 200) {
            throw new Error('Post情報の取得に失敗しました')
        }

        postStore.convertResponseToPost(response.data)
    } catch (error) {
        console.error(error)
    }

    isLoadImages.value = false
}
// 画像のダウンロード
const dlImage = async () => {
    isLoadImages.value = true
    const images = postStore.extractImages(postStore.posts)

    // 画像URL一覧をAPIに送り画像をDL
    const response = await axios.post(`${endPoint}/download/image`, {
        images: images,
        platform: platform,
    })

    if (response.status !== 200) {
        throw new Error('画像情報の取得に失敗しました')
    }

    const link = document.createElement('a')
    link.href = `${endPoint}/download/zip?timestamp=${response.data.now_time}&platform=${platform.value}`
    link.target = '_blank'
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)

    await updateCounter(images.length)
    await createDownloadLog()

    isLoadImages.value = false
}

// ダウンロード数の更新
const updateCounter = async (get_images_count: number) => {
    const response = await axios.post(
        `${endPoint}/userPlatformAccount/update/${userId}`,
        {
            platform: platform,
            get_images_count: get_images_count,
        }
    )
    return response
}

// ダウンロードログの追加
const createDownloadLog = async () => {
    const response = await axios.post(
        `${endPoint}/userPlatformAccountDlLog/insert`,
        {
            user_id: userId,
            platform: platform,
            post_id: postStore.posts.map((post) => post.id),
        }
    )
    return response
}
</script>
<template>
    <HeaderComponent />
    <main class="main-container twi-template">
        <section class="common-form">
            <div class="switch-platform">
                <a
                    @click="switchPlatform('twitter')"
                    class="btn-small green"
                    v-if="platform === 'pixiv'"
                >
                    pixiv
                </a>
                <a
                    @click="switchPlatform('pixiv')"
                    class="btn-small green"
                    v-if="platform === 'twitter'"
                >
                    twitter
                </a>
            </div>
            <SearchPixivForm
                v-if="platform === 'pixiv'"
                :search="searchStore.pixivSearch"
                @getPosts="getPosts()"
            />
            <SearchTwitterForm
                v-if="platform === 'twitter'"
                :search="searchStore.twitterSearch"
                @getPosts="getPosts()"
            />
            <ButtonComponent
                @click="getPosts()"
                text="投稿を取得"
                :buttonClass="'btn-common green get-posts'"
            />
            <div v-show="isLoadImages" class="btn-cover"></div>
        </section>
        <p>{{ errorMessage }}</p>
        <section v-if="postStore.posts.length > 0" class="post-list">
            <div v-show="isLoadImages" class="btn-cover"></div>
            <div class="title-area">
                <h2>取得投稿一覧</h2>
                <p v-if="postStore.posts.length > 0" class="caption">
                    取得投稿数: {{ postStore.posts.length }}
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
            <div class="post-list twitter" v-if="platform === 'twitter'">
                <TwitterPost
                    v-for="post in postStore.posts"
                    :key="post.id"
                    :post="post"
                />
            </div>
            <div class="post-list pixiv" v-if="platform === 'pixiv'">
                <PixivPost
                    v-for="post in postStore.posts"
                    :key="post.id"
                    :post="post"
                />
            </div>
        </section>
    </main>
</template>
