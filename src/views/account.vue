<script setup lang="ts">
import HeaderComponent from '@/components/HeaderComponent.vue'
import ButtonComponent from '@/components/ButtonComponent.vue'

import '@/assets/scss/account.scss'

import { ref, onMounted } from 'vue'
import ApiManager from '@/server/apiManager'
import { apiPath } from '@/assets/ts/paths'
import { UserInfo } from '@/types'

const isOpenTwitter = ref<boolean>(false)
const isOpenPixiv = ref<boolean>(false)

const userInfo = ref<UserInfo>({
    created_at: '',
    updated_at: '',
    dl_count: 0,
    images_count: 0,
    pixiv: [],
    twitter: [],
    twitter_password: '',
    user_name: '',
})
const apiManager = new ApiManager()
const getUserInfo = async () => {
    const response = await apiManager.get(`${apiPath}/api/getUserInfo`)
    return response.content.content
}

const saveUserInfo = async () => {
    const response = await apiManager.post(`${apiPath}/api/updateUserInfo`, {
        user_name: userInfo.value.user_name,
        twitter_password: userInfo.value.twitter_password,
    })

    if (!response.error) userInfo.value = await getUserInfo()
}

const deleteUserInfo = async () => {
    if (!confirm('アカウントを削除しますか？')) return

    const response = await apiManager.post(`${apiPath}/api/deleteUserInfo`)

    if (!response.error) {
        alert('アカウントを削除しました。')
        userInfo.value = await getUserInfo()
    }
}

onMounted(async () => {
    userInfo.value = await getUserInfo()
})
</script>

<template>
    <HeaderComponent />
    <main id="page-account">
        <div>
            <h2>ユーザー情報の登録・編集</h2>
            <dl class="form-box">
                <div>
                    <dt>ユーザー名</dt>
                    <dd><input type="text" v-model="userInfo.user_name" /></dd>
                </div>
                <div>
                    <dt>Twitterパスワード</dt>
                    <dd>
                        <input
                            type="text"
                            v-model="userInfo.twitter_password"
                        />
                    </dd>
                </div>
                <ButtonComponent
                    @click="saveUserInfo()"
                    :buttonClass="'btn-common green'"
                    :text="'保存'"
                />
            </dl>
        </div>
        <div>
            <h2>その他のユーザー情報</h2>
            <dl class="form-box">
                <div>
                    <dt>ダウンロード回数</dt>
                    <dd>
                        <p>{{ userInfo.dl_count }}</p>
                    </dd>
                </div>
                <div>
                    <dt>ダウンロードした画像の枚数</dt>
                    <dd>
                        <p>{{ userInfo.images_count }}</p>
                    </dd>
                </div>
                <div>
                    <dt>アカウント登録日</dt>
                    <dd>
                        <p>{{ userInfo.created_at }}</p>
                    </dd>
                </div>
                <div>
                    <dt>アカウント更新日</dt>
                    <dd>
                        <p>{{ userInfo.updated_at }}</p>
                    </dd>
                </div>
                <div>
                    <dt>Twitter</dt>
                    <dd>
                        <p v-if="!isOpenTwitter" @click="isOpenTwitter = true">
                            開く ▼
                        </p>
                        <p v-if="isOpenTwitter" @click="isOpenTwitter = false">
                            閉じる ▲
                        </p>
                        <ul v-if="isOpenTwitter" class="get-post-list">
                            <li
                                v-for="(data, index) in userInfo.twitter"
                                :key="index"
                            >
                                <p>ユーザーID: {{ data.id }}</p>
                                <p>投稿ID: {{ data.post }}</p>
                            </li>
                        </ul>
                    </dd>
                </div>
                <div>
                    <dt>pixiv</dt>
                    <dd>
                        <p v-if="!isOpenPixiv" @click="isOpenPixiv = true">
                            開く ▼
                        </p>
                        <p v-if="isOpenPixiv" @click="isOpenPixiv = false">
                            閉じる ▲
                        </p>
                        <ul v-if="isOpenPixiv" class="get-post-list">
                            <li
                                v-for="(data, index) in userInfo.pixiv"
                                :key="index"
                            >
                                <p>
                                    ユーザーID:
                                    {{ data.id !== '' ? data.id : '未設定' }}
                                </p>
                                <p>
                                    タグ名:
                                    {{ data.tag !== '' ? data.tag : '未設定' }}
                                </p>
                                <p>投稿ID: {{ data.post }}</p>
                            </li>
                        </ul>
                    </dd>
                </div>
            </dl>
        </div>
        <ButtonComponent
            @click="deleteUserInfo()"
            :buttonClass="'btn-common red'"
            :text="'アカウント削除'"
        />
    </main>
</template>
