import { ref } from 'vue'
import { defineStore } from 'pinia'
import { UserInfo } from '@/types'

export const useUserStore = defineStore('user', () => {
    const userInfo = ref<UserInfo>({
        id: 0,
        user_name: '',
        email: '',
        uuid: '',
        created_at: '',
        updated_at: '',
    })

    return { userInfo }
})
