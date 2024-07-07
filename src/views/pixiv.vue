<script setup lang="ts">
import HeaderComponent from '@/components/HeaderComponent.vue'
import ButtonComponent from '@/components/ButtonComponent.vue'

import axios from 'axios'
import { ref } from 'vue'
import { createEndPoint } from '@/assets/ts/paths'
import { PixivPost, PixivPostImage } from '@/types/pixiv'
import { usePixivStore } from '@/store/pixivStore'

import '@/assets/scss/pixForm.scss'

const errorMessage = ref<string>('')
const pixivStore = usePixivStore()

const searchQuery = pixivStore.searchQuery
const endPoint = createEndPoint('/api/pixiv')

// 入力フォームのバリデーション
const inputValidation = (): string => {
    let error = ''
    if (searchQuery.userID === null || searchQuery.userID === 0) {
        error = 'ユーザーIDが入力されていません。'
    }

    const numPost = parseInt(searchQuery.getNumberOfPost)
    if (isNaN(numPost)) {
        error = '取得作品数は数値で入力してください。'
    }
    if (numPost < 10 || numPost > 300) {
        error = '取得できる作品の最小値は10, 最大値は300です。'
    }
    return error
}

const pixivPosts = ref<PixivPost[]>([])
const isLoadImages = ref<boolean>(false)
const dlName = ref<string>('')
// 画像情報の取得
const getImage = async () => {
    isLoadImages.value = true
    errorMessage.value = inputValidation()
    if (errorMessage.value !== '') return

    try {
        const response = await axios.get(`${endPoint}/getPost`, {
            params: searchQuery,
        })

        if (response.status !== 200) {
            throw new Error('画像情報の取得に失敗しました')
        }

        pixivPosts.value = response.data.map((post: PixivPost) => {
            return {
                postID: post.postID,
                post_time: post.post_time,
                user: post.user,
                text: post.text,
                url: post.url,
                images: post.images.map(
                    (image: PixivPostImage, index: number) => {
                        return {
                            id: `${post.postID}_${index}`,
                            url: image,
                            selected: true,
                        }
                    }
                ),
            }
        })
    } catch (error) {
        console.error(error)
    }

    isLoadImages.value = false
    dlName.value = searchQuery.tag !== '' ? searchQuery.tag : ''
}

// 画像のダウンロード
const dlImage = async () => {
    isLoadImages.value = true

    // 画像URL一覧をAPIに送り画像をDL
    const response = await axios.post(`${endPoint}/download`, {
        illust: pixivPosts.value,
    })

    if (response.status !== 200) {
        throw new Error('画像情報の取得に失敗しました')
    }

    const link = document.createElement('a')
    link.href = response.data.zip_path
    document.body.appendChild(link)
    link.click()
    link.setAttribute('download', ``)
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
                        取得内容
                        <em>*</em>
                    </dt>
                    <dd class="radio-list">
                        <div>
                            <input
                                id="get-bookmark"
                                v-model="searchQuery.getPostType"
                                type="radio"
                                value="bookmark"
                            />
                            <label for="get-bookmark">ブックマーク</label>
                        </div>
                        <div>
                            <input
                                id="get-post"
                                v-model="searchQuery.getPostType"
                                type="radio"
                                value="post"
                            />
                            <label for="get-post">作品</label>
                        </div>
                        <div>
                            <input
                                id="get-keyword"
                                v-model="searchQuery.getPostType"
                                type="radio"
                                value="tag"
                            />
                            <label for="get-keyword">タグ</label>
                        </div>
                    </dd>
                </div>
                <div v-if="searchQuery.getPostType === 'tag'">
                    <dt>タグキーワード</dt>
                    <dd>
                        <input type="text" id="tag" v-model="searchQuery.tag" />
                    </dd>
                </div>
                <div v-if="searchQuery.getPostType === 'tag'">
                    <dt>ブックマーク数下限</dt>
                    <dd>
                        <input
                            type="number"
                            id="min-bookmark"
                            v-model="searchQuery.minBookmarks"
                        />
                    </dd>
                </div>
                <div v-else>
                    <dt>ユーザーID</dt>
                    <dd>
                        <input
                            type="number"
                            id="user-id"
                            v-model="searchQuery.userID"
                        />
                    </dd>
                </div>
                <div>
                    <dt>取得投稿数</dt>
                    <dd>
                        <input
                            type="number"
                            id="get-post-num"
                            v-model="searchQuery.getNumberOfPost"
                        />
                    </dd>
                </div>
                <div>
                    <dt>詳細設定</dt>
                    <dd>
                        <input
                            id="get-pre"
                            v-model="searchQuery.isGetFromPreviousPost"
                            type="checkbox"
                        />
                        <label for="get-pre">取得を中断するIDを設定</label>
                        <input
                            id="include-tags"
                            v-model="searchQuery.includeTags"
                            type="checkbox"
                        />
                        <label for="include-tags">タグフィルターを設定</label>
                        <input
                            id="ignore-sensitive"
                            v-model="searchQuery.isIgnoreSensitive"
                            type="checkbox"
                        />
                        <label for="ignore-sensitive">R-18作品を除外する</label>
                    </dd>
                </div>
                <div v-show="isLoadImages" class="btn-cover"></div>
                <ButtonComponent
                    @click="getImage()"
                    text="作品を取得"
                    :buttonClass="'btn-common green'"
                />
            </dl>
        </section>
        <p>{{ errorMessage }}</p>
        <section v-if="pixivPosts.length > 0" class="post-list">
            <div v-show="isLoadImages" class="btn-cover"></div>
            <div class="title-area">
                <h2>取得投稿一覧</h2>
                <p v-if="pixivPosts.length > 0" class="caption">
                    取得投稿数: {{ pixivPosts.length }}
                </p>
            </div>
            <div class="dl-image-area">
                <label for="dl-name">保存名</label>
                <input type="text" id="dl-name" v-model="dlName" />
                <ButtonComponent
                    @click="dlImage()"
                    text="ダウンロード"
                    :buttonClass="'btn-common green'"
                />
                <p class="caption">※選択している画像をDLします。</p>
            </div>
            <div
                v-for="pixPost in pixivPosts"
                :key="pixPost.postID"
                class="post-info"
            >
                <h3 class="user-name">{{ pixPost.user }}</h3>
                <p class="pix-post-text">{{ pixPost.text }}</p>
                <div class="pix-post-image">
                    <div
                        v-for="(image, index) in pixPost.images"
                        :key="image.id"
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
                            {{ `${index + 1}枚目: ${image.id}` }}
                        </label>
                    </div>
                </div>
                <div class="post-url">
                    <p>作品元リンク</p>
                    <a :href="pixPost.url">{{ pixPost.url }}</a>
                </div>
            </div>
        </section>
    </main>
</template>
