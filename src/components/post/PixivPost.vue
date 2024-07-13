<script setup lang="ts">
import { ref, defineProps } from 'vue'
import '@/assets/scss/imagedler/posts/pixiv.scss'
import { Post } from '@/types/post'

const props = defineProps<{
    post: Post
}>()

const post = ref<Post>(props.post)
</script>

<template>
    <div class="post-info">
        <h3 class="user-name">{{ post.user }}</h3>
        <p class="post-text">{{ post.text }}</p>
        <div class="post-image">
            <div v-for="(image, index) in post.images" :key="image.id">
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
            <a :href="post.url">{{ post.url }}</a>
        </div>
    </div>
</template>
