<script setup lang="ts">
import { ref } from 'vue'
import { TwitterSearch } from '@/types/search'
import '@/assets/scss/commonForm.scss'

const props = defineProps<{
    search: TwitterSearch
}>()

const search = ref<TwitterSearch>(props.search)
</script>

<template>
    <dl class="form-box">
        <div>
            <dt>
                Twitter ID
                <em>*</em>
            </dt>
            <dd><input v-model="search.id" type="text" /></dd>
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
                        v-model="search.type"
                        type="radio"
                        value="liked_tweets"
                    />
                    <label for="get-like">いいね</label>
                </div>
                <div>
                    <input
                        id="get-tweet"
                        v-model="search.type"
                        type="radio"
                        value="tweets"
                        disabled
                    />
                    <label for="get-tweet">ツイート</label>
                </div>
                <div>
                    <input
                        id="get-bookmark"
                        v-model="search.type"
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
            </dt>
            <dd>
                <input
                    v-model="search.getNumberOfPost"
                    type="number"
                    min="1"
                    max="300"
                />
            </dd>
        </div>
        <div>
            <dt>詳細設定</dt>
            <dd>
                <input
                    id="get-pre"
                    v-model="search.isGetFromPreviousPost"
                    type="checkbox"
                />
                <label for="get-pre">前回DLした画像以降を取得</label>
            </dd>
        </div>
    </dl>
</template>
