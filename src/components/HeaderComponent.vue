<script setup lang="ts">
import '@/assets/scss/header.scss'
import { useUserStore } from '@/store/userStore'

const userStore = useUserStore()
const user = userStore.user
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
                <a href="./" class="btn-small blue">アカウント管理</a>
                <a href="./imagedler" class="btn-small blue">imagedler</a>
            </nav>
        </div>
        <div class="header-account">
            <div v-if="user.user_name !== ''">
                <p>{{ user.user_name }}さん</p>
            </div>
            <div v-else>
                <a href="./account" class="btn-small green">アカウント登録</a>
            </div>
        </div>
    </header>
</template>
