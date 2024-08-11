<script setup lang="ts">
import HeaderComponent from '@/components/HeaderComponent.vue'
import ButtonComponent from '@/components/ButtonComponent.vue'

import { ref, computed, onMounted } from 'vue'
import { useTagStore } from '@/store/tagStore'
import { createEndPoint } from '@/assets/ts/paths'
import { Tag } from '@/types/tag'

import '@/assets/scss/master.scss'

const endPoint = createEndPoint('/api/tag')
const tagStore = useTagStore()

const tags = computed(() => tagStore.tags)
const selectedTag = computed(() => {
    const tag = tags.value.find((tag) => tag.id === selectedId.value)
    return [
        { name: 'id', value: tag?.id, edit: false },
        { name: 'category_id', value: tag?.category_id, edit: 'select' },
        { name: '英名', value: tag?.name_en, edit: 'text' },
        { name: '日本語名', value: tag?.name_ja, edit: 'text' },
        { name: '登録日時', value: tag?.created_at, edit: false },
        { name: '更新日時', value: tag?.updated_at, edit: false },
    ]
})

const selectedId = ref<number>(-1)
const headers = ref([
    { name_en: 'id', name_ja: null },
    { name_en: 'category_id', name_ja: null },
    { name_en: 'name_en', name_ja: '英名' },
    { name_en: 'name_ja', name_ja: '日本語名' },
])

const truncateText = (text: string, length = 30) => {
    return text.length > length ? text.slice(0, length) + '...' : text
}

onMounted(async () => {
    await tagStore.getTags()
})
</script>

<template>
    <HeaderComponent />
    <main id="page-master">
        <v-container class="main-container">
            <v-table density="compact" class="tags">
                <thead>
                    <tr>
                        <th>checkbox</th>
                        <th v-for="header in headers" :key="header.name_en">
                            {{ header.name_ja ?? header.name_en }}
                        </th>
                    </tr>
                </thead>
                <tbody>
                    <tr
                        v-for="tag in tags"
                        :key="tag.id"
                        :class="{ selected: tag.id === selectedId }"
                        class="item"
                        @click="selectedId = tag.id"
                    >
                        <td class="text-center py-1">
                            <input type="checkbox" v-model="tag.selected" />
                        </td>
                        <td class="text-center py-1">{{ tag.id }}</td>
                        <td class="text-center py-1">{{ tag.category_id }}</td>
                        <td class="text-center py-1">
                            {{ truncateText(tag.name_en) }}
                        </td>
                        <td class="text-center py-1">
                            {{ tag.name_ja ?? '未設定' }}
                        </td>
                    </tr>
                </tbody>
            </v-table>
            <v-list class="tag-info" elevation="2">
                <v-list-item
                    v-for="(data, index) in selectedTag"
                    :key="index"
                    class="item"
                >
                    <v-list-item-title class="title">
                        {{ data.name }}
                    </v-list-item-title>
                    <v-list-item-subtitle class="content">
                        {{ data.value ?? '-' }}
                    </v-list-item-subtitle>
                </v-list-item>
            </v-list>
        </v-container>
    </main>
</template>
