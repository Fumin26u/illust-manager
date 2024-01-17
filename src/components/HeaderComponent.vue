<script setup lang="ts">
import { ref, onMounted } from 'vue'
import ApiManager from '@/server/apiManager'
import { apiPath } from '@/assets/ts/paths'
import '@/assets/scss/imagedler/header.scss'
import {
    VMenu,
    VList,
    VListItem,
    VListItemTitle,
    VBtn,
} from 'vuetify/components'

const username = ref<string>('')
// ログアウトリンクが押された場合APIに伝える
const apiManager = new ApiManager()

const getUserInfo = async () => {
    const response = await apiManager.get(`${apiPath}/api/getUserName`)
    return response.content.content
}

// 画面読み込み時にログインユーザーIDを取得
onMounted(async () => {
    username.value = await getUserInfo()
})

const imageLinks = ref<any>([
    {
        name: 'アカウント管理',
        path: './account',
    },
    {
        name: '画像加工',
        path: './crop',
    },
    {
        name: '画像評価',
        path: './evaluate',
    },
    {
        name: 'モデル訓練',
        path: './train',
    },
    {
        name: '被り削除',
        path: './remove',
    },
])

const imageDLerLinks = [
    {
        name: 'twitter',
        path: './twitter',
    },
    {
        name: 'pixiv',
        path: './pixiv',
    },
]
</script>

<template>
    <header class="header-container">
        <div class="header-left">
            <div class="title-area">
                <a href="./">
                    <h1>IllustManager(仮)</h1>
                    <p class="caption">イラスト保存・管理統合ツール(仮)</p>
                </a>
            </div>
            <nav class="header-nav">
                <a href="./account" class="btn-small blue">アカウント管理</a>
                <v-menu
                    open-on-hover
                    offset-y
                    :open-delay="50"
                    :close-delay="50"
                >
                    <template v-slot:activator="{ props }">
                        <p v-bind="props">画像処理</p>
                    </template>

                    <v-list>
                        <v-list-item
                            v-for="(imageLink, index) in imageLinks"
                            :key="index"
                            link
                            :href="imageLink.path"
                        >
                            <v-list-item-title>
                                {{ imageLink.name }}
                            </v-list-item-title>
                        </v-list-item>
                    </v-list>
                </v-menu>
                <v-menu
                    open-on-hover
                    offset-y
                    :open-delay="50"
                    :close-delay="50"
                >
                    <template v-slot:activator="{ props }">
                        <p v-bind="props">ImageDLer</p>
                    </template>

                    <v-list>
                        <v-list-item
                            v-for="(imageDLerLink, index) in imageDLerLinks"
                            :key="index"
                            link
                            :href="imageDLerLink.path"
                        >
                            <v-list-item-title>
                                {{ imageDLerLink.name }}
                            </v-list-item-title>
                        </v-list-item>
                    </v-list>
                </v-menu>
            </nav>
        </div>
        <div class="header-account">
            <div v-if="username !== ''">
                <p>{{ username }}さん</p>
            </div>
            <div v-else>
                <a href="./account" class="btn-common green">アカウント登録</a>
            </div>
        </div>
    </header>
</template>
