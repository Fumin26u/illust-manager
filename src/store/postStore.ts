import { ref } from 'vue'
import { defineStore } from 'pinia'
import { Post, Image } from '@/types/post'

export const usePostStore = defineStore('post', () => {
    const posts = ref<Post[]>([])

    const convertResponseToPost = (responseData: any): void => {
        posts.value = responseData.map((post: Post) => {
            return {
                id: post.id,
                created_at: post.created_at,
                user: post.user,
                text: post.text,
                url: post.url,
                images: post.images.map((image: Image, index: number) => {
                    return {
                        id: `${post.id}_${index}`,
                        url: image,
                        selected: true,
                    }
                }),
            }
        })
    }

    const extractImages = (posts: Post[]) => {
        const images: string[] = []
        posts.map((post) => {
            post.images.map((image: Image) => {
                if (image.selected) images.push(image.url)
            })
        })
        return images
    }

    return { posts, convertResponseToPost, extractImages }
})
