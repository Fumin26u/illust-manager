import { ref } from 'vue'
import { defineStore } from 'pinia'
import { User } from '@/types/user'

export const useUserStore = defineStore('user', () => {
    const user = ref<User>({
        id: 1,
        user_name: '',
        email: '',
        uuid: '',
        created_at: '',
        updated_at: '',
    })

    return { user }
})
