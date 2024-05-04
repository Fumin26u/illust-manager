import { ref } from 'vue'
import { defineStore } from 'pinia'
import { UserInfo } from '@/types'

export const useAccountStore = defineStore('account', () => {
    const userInfo = ref<UserInfo>({
        created_at: '',
        updated_at: '',
        dl_count: 0,
        images_count: 0,
        pixiv: [],
        twitter: [],
        twitter_password: '',
        pixiv_password: '',
        user_name: '',
    })

    return { userInfo }
})
