<script setup lang="ts">
import { ref, onMounted } from 'vue'
import ApiManager from '@/server/apiManager'
import { apiPath } from '@/assets/ts/paths'
import '@/assets/scss/imagedler/header.scss'

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

const isCharaMenuVisible = ref<boolean>(false)
const isImageMenuVisible = ref<boolean>(false)
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
                <div
                    @mouseover="isCharaMenuVisible = true"
                    @mouseleave="isCharaMenuVisible = false"
                >
                    <p>画像処理</p>
                    <div
                        class="nav-menu edit-image"
                        v-show="isCharaMenuVisible"
                    >
                        <a href="./crop" class="btn-small blue">画像加工</a>
                        <a href="./evaluate" class="btn-small blue">画像評価</a>
                        <a href="./train" class="btn-small blue">モデル訓練</a>
                        <a href="./remove" class="btn-small blue">被り削除</a>
                    </div>
                </div>
                <div
                    @mouseover="isImageMenuVisible = true"
                    @mouseleave="isImageMenuVisible = false"
                >
                    <p>ImageDLer</p>
                    <div class="nav-menu imagedler" v-show="isImageMenuVisible">
                        <a href="./twitter" class="btn-small blue">twitter</a>
                        <a href="./pixiv" class="btn-small blue">pixiv</a>
                    </div>
                </div>
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
