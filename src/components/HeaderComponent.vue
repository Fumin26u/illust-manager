<script setup lang="ts">
import { ref, onMounted } from 'vue'
import ApiManager from '@/server/apiManager'
import { apiPath } from '@/assets/ts/paths'
import '@/assets/scss/imagedler/header.scss'

const username = ref<string>('')
// ログアウトリンクが押された場合APIに伝える
const apiManager = new ApiManager()

const getUserInfo = async () => {
    const response = await apiManager.get(`${apiPath}/api/getAccount`)
    return response.content
}

// 画面読み込み時にログインユーザーIDを取得
onMounted(async () => {
    username.value = await getUserInfo()
})
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
                <a href="./evaluate" class="btn-small blue">評価</a>
                <a href="./training" class="btn-small blue">訓練</a>
                <a href="./twitter" class="btn-small blue">twitter</a>
                <a href="./pixiv" class="btn-small blue">pixiv</a>
                <a href="./account" class="btn-small blue">アカウント管理</a>
            </nav>
        </div>
        <div class="header-account">
            <div v-if="username !== ''">
                <p>{{ username }}さん</p>
            </div>
            <div v-else>
                <a href="./#/register-pre" class="btn-common green">
                    アカウント登録
                </a>
            </div>
        </div>
    </header>
</template>
