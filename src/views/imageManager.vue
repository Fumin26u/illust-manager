<script setup lang="ts">
import HeaderComponent from '@/components/HeaderComponent.vue'
import ButtonComponent from '@/components/ButtonComponent.vue'

import axios from '@/axios'
import { ref } from 'vue'
import { createEndPoint } from '@/assets/ts/paths'
import { useSearchStore } from '@/store/searchStore'
import { usePostStore } from '@/store/postStore'
</script>
<template>
    <HeaderComponent />
    <main class="main-container image-manager">
        <section class="import-image">
            <h2>画像のインポート</h2>
            <div>
                <input type="file" />
            </div>
        </section>
    </main>
</template>
