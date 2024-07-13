<script setup lang="ts">
import { ref, defineProps } from 'vue'
import { Post } from '@/types/post'
import '@/assets/scss/imagedler/posts/twitter.scss'

const props = defineProps<{
    post: Post
}>()

const post = ref<Post>(props.post)
</script>

<template>
    <div class="post-info">
        <h3 class="user-name">{{ post.user }}</h3>
        <p class="post-text">{{ post.text }}</p>
        <div v-for="image in post.images" :key="image.id" class="post-image">
            <input :id="image.id" v-model="image.selected" type="checkbox" />
            <label
                :for="image.id"
                :class="!image.selected ? 'not-selected' : ''"
            >
                <img :src="image.url" :alt="post.text" />
            </label>
        </div>
        <div class="post-url">
            <a :href="post.url">ツイート元リンク</a>
        </div>
    </div>
</template>
