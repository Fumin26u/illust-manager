<script setup lang="ts">
import { ref } from 'vue'
import { PixivSearch } from '@/types/search'
import '@/assets/scss/commonForm.scss'

const props = defineProps<{
    search: PixivSearch
}>()

const search = ref<PixivSearch>(props.search)
</script>

<template>
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
                        v-model="search.type"
                        type="radio"
                        value="bookmark"
                    />
                    <label for="get-bookmark">ブックマーク</label>
                </div>
                <div>
                    <input
                        id="get-post"
                        v-model="search.type"
                        type="radio"
                        value="post"
                    />
                    <label for="get-post">作品</label>
                </div>
                <div>
                    <input
                        id="get-keyword"
                        v-model="search.type"
                        type="radio"
                        value="tag"
                    />
                    <label for="get-keyword">タグ</label>
                </div>
            </dd>
        </div>
        <div v-if="search.type === 'tag'">
            <dt>タグキーワード</dt>
            <dd>
                <input type="text" id="tag" v-model="search.tag" />
            </dd>
        </div>
        <div v-if="search.type === 'tag'">
            <dt>ブックマーク数下限</dt>
            <dd>
                <input
                    type="number"
                    id="min-bookmark"
                    v-model="search.minBookmarks"
                />
            </dd>
        </div>
        <div v-else>
            <dt>ユーザーID</dt>
            <dd>
                <input type="number" id="user-id" v-model="search.id" />
            </dd>
        </div>
        <div>
            <dt>取得投稿数</dt>
            <dd>
                <input
                    type="number"
                    id="get-post-num"
                    v-model="search.getNumberOfPost"
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
                <label for="get-pre">取得を中断するIDを設定</label>
                <input
                    id="include-tags"
                    v-model="search.includeTags"
                    type="checkbox"
                />
                <label for="include-tags">タグフィルターを設定</label>
                <input
                    id="ignore-sensitive"
                    v-model="search.isIgnoreSensitive"
                    type="checkbox"
                />
                <label for="ignore-sensitive">R-18作品を除外する</label>
            </dd>
        </div>
    </dl>
</template>
