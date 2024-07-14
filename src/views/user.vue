<script setup lang="ts">
import HeaderComponent from '@/components/HeaderComponent.vue'
import ButtonComponent from '@/components/ButtonComponent.vue'

import '@/assets/scss/user.scss'

import axios from '@/axios'
import { createEndPoint } from '@/assets/ts/paths'
import { useUserStore } from '@/store/userStore'

const userStore = useUserStore()

const user = userStore.user
const endPoint = createEndPoint('/api/user')

const saveUser = async () => {
    try {
        const response = await axios.put(`${endPoint}`, user)
        if (response.status !== 200) {
            throw new Error('ユーザー情報の更新に失敗しました')
        }

        userStore.getUser()
    } catch (error) {
        console.error(error)
    }
}
</script>

<template>
    <HeaderComponent />
    <main id="page-account">
        <div>
            <h2>ユーザー情報の登録・編集</h2>
            <dl class="form-box">
                <div>
                    <dt>ユーザー名</dt>
                    <dd><input type="text" v-model="user.user_name" /></dd>
                </div>
                <div>
                    <dt>メールアドレス</dt>
                    <dd><input type="text" v-model="user.email" /></dd>
                </div>
                <ButtonComponent
                    @click="saveUser()"
                    :buttonClass="'btn-common green'"
                    :text="'保存'"
                />
            </dl>
        </div>
        <div>
            <h2>その他のユーザー情報</h2>
            <dl class="form-box">
                <div>
                    <dt>アカウント登録日</dt>
                    <dd>
                        <p>{{ user.created_at }}</p>
                    </dd>
                </div>
                <div>
                    <dt>アカウント更新日</dt>
                    <dd>
                        <p>{{ user.updated_at }}</p>
                    </dd>
                </div>
            </dl>
        </div>
    </main>
</template>
