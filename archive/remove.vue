<script setup lang="ts">
import HeaderComponent from '@/components/HeaderComponent.vue'
import ButtonComponent from '@/components/ButtonComponent.vue'

import '@/assets/scss/remove.scss'

import { ref, onMounted } from 'vue'
import ApiManager from '@/server/apiManager'
import { apiPath } from '@/assets/ts/paths'
import { UserInfo } from '@/types/types/types'
</script>

<template>
    <HeaderComponent />
    <main id="page-remove"></main>
</template>
