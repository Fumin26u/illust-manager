<script setup lang="ts">
import HeaderComponent from '@/components/HeaderComponent.vue'

import { ref, computed, onMounted } from 'vue'
import { useTagStore } from '@/store/tagStore'
import { createEndPoint } from '@/assets/ts/paths'

import '@/assets/scss/master.scss'

const endPoint = createEndPoint('/api/tag')
const tagStore = useTagStore()

const tags = computed(() => tagStore.tags)
const selectedTag = computed(() =>
    tags.value.find((tag) => tag.id === selectedId.value)
)
const displaySelectedTag = computed(() => {
    const tag = tags.value.find((tag) => tag.id === selectedId.value)
    return [
        { name: 'id', value: tag?.id, edit: false },
        { name: 'category_id', value: tag?.category_id, edit: 'select' },
        { name: '英名', value: tag?.name_en, edit: false },
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
const searchString = ref<string>('')

const truncateText = (text: string, length = 30) => {
    return text.length > length ? text.slice(0, length) + '...' : text
}

const search = async () => await tagStore.search(searchString.value)
const update = async () => {
    if (selectedTag.value) {
        await tagStore.updateTag(selectedTag.value)
    }
}

onMounted(async () => {
    await tagStore.getTags()
})
</script>

<template>
    <HeaderComponent />
    <main id="page-master" class="main-container">
        <v-form class="search-form">
            <v-col cols="12" sm="10" md="8" lg="6">
                <v-row>
                    <v-col cols="9">
                        <v-text-field
                            v-model="searchString"
                            label="タグを検索"
                            variant="underlined"
                            hide-details
                            required
                        ></v-text-field>
                    </v-col>
                    <v-col cols="3" class="d-flex align-end">
                        <v-btn
                            @click="search()"
                            color="secondary"
                            density="comfortable"
                        >
                            検索
                        </v-btn>
                    </v-col>
                </v-row>
            </v-col>
        </v-form>
        <section class="tags-detail">
            <v-table density="compact" class="tags">
                <thead>
                    <tr>
                        <th class="text-center">checkbox</th>
                        <th
                            v-for="header in headers"
                            :key="header.name_en"
                            class="text-center"
                        >
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
            <v-container class="tag-info">
                <v-container class="top-button-area">
                    <v-btn color="secondary" @click="selectedId = -1">
                        新規作成
                    </v-btn>
                </v-container>
                <v-list elevation="2">
                    <v-list-item
                        v-for="(data, index) in displaySelectedTag"
                        :key="index"
                        class="item"
                    >
                        <v-list-item-title class="title">
                            {{ data.name }}
                        </v-list-item-title>
                        <v-text-field
                            v-if="selectedId !== -1 && data.edit === 'text'"
                            v-model="selectedTag.name_ja"
                            :value="data.value"
                            variant="underlined"
                            hide-details
                        ></v-text-field>
                        <v-list-item-subtitle v-else class="content">
                            {{ data.value ?? '-' }}
                        </v-list-item-subtitle>
                    </v-list-item>
                    <v-container class="top-button-area">
                        <v-btn
                            v-if="selectedId !== -1"
                            color="primary"
                            @click="update()"
                        >
                            更新
                        </v-btn>
                    </v-container>
                </v-list>
            </v-container>
        </section>
    </main>
</template>
