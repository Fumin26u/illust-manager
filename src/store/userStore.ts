import { ref } from 'vue'
import { defineStore } from 'pinia'
import { User } from '@/types/user'
import { createEndPoint } from '@/assets/ts/paths'
import axios from 'axios'

export const useUserStore = defineStore('user', () => {
    const user = ref<User>({
        id: 1,
        user_name: '',
        email: '',
        uuid: '',
        created_at: '',
        updated_at: '',
    })

    const getUser = async (endPoint = createEndPoint('/api/user')) => {
        try {
            const response = await axios.get(`${endPoint}/${user.value.id}`)
            user.value = response.data
            console.log(response.data)
        } catch (error) {
            console.error(error)
        }
    }

    return { user, getUser }
})
