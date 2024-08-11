<script setup lang="ts">
import HeaderComponent from '@/components/HeaderComponent.vue'

import { ref, computed, onMounted } from 'vue'
import { useTagStore } from '@/store/tagStore'
import { createEndPoint } from '@/assets/ts/paths'

import '@/assets/scss/master.scss'

const tagStore = useTagStore()
const initTag = {
    selected: false,
    id: -1,
    category_id: 1,
    name_en: '',
    name_ja: '',
    words: [],
    is_deprecated: false,
    post_count: 0,
    created_at: '',
    updated_at: '',
}

const tags = computed(() => tagStore.tags ?? [{ ...initTag }])
const categories = computed(() => tagStore.categories)
const selectedTag = computed(
    () =>
        tags.value.find((tag) => tag.id === selectedId.value) ?? { ...initTag }
)

const selectedId = ref<number>(-1)
const headers = ref([
    { name_en: 'id', name_ja: null },
    { name_en: 'category_id', name_ja: null },
    { name_en: 'name_en', name_ja: '英名' },
    { name_en: 'name_ja', name_ja: '日本語名' },
])
const searchString = ref<string>('')
const dialog = ref<boolean>(false)

const truncateText = (text: string, length = 24) => {
    return text.length > length ? text.slice(0, length) + '...' : text
}

const search = async () => {
    selectedId.value = -1
    await tagStore.search(searchString.value)
}
const update = async () => {
    if (selectedTag.value) {
        await tagStore.updateTag(selectedTag.value)
    }
}

const selectedCategoryId = ref<number>(1)
const updateTagCategoryIds = async () => {
    const selectedTags = tags.value.filter((tag) => tag.selected)
    await tagStore.updateTagCategoryIds(selectedTags, selectedCategoryId.value)
    dialog.value = false
}

onMounted(async () => {
    await tagStore.getTags()
    await tagStore.getCategories()
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
                        <th class="text-center checkbox">選択</th>
                        <th
                            v-for="header in headers"
                            :key="header.name_en"
                            class="text-center"
                            :class="header.name_en"
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
                        <td class="text-center py-1 checkbox">
                            <input
                                type="checkbox"
                                :id="tag.name_en"
                                v-model="tag.selected"
                            />
                        </td>
                        <td class="text-center py-1 id">{{ tag.id }}</td>
                        <td class="text-center py-1 category_id">
                            {{ tag.category_id }}
                        </td>
                        <td class="text-center py-1 name_en">
                            {{ truncateText(tag.name_en) }}
                        </td>
                        <td class="text-center py-1 name_ja">
                            {{ tag.name_ja ?? '未設定' }}
                        </td>
                    </tr>
                </tbody>
                <v-container>
                    <v-btn color="primary" class="open-dialog">一括更新</v-btn>
                    <v-dialog v-model="dialog" activator="parent">
                        <v-card>
                            <v-card-title>タグの一括更新</v-card-title>
                            <v-card-text>
                                <p class="my-4">
                                    選択したタグのカテゴリーを一括更新:
                                </p>
                                <select v-model="selectedCategoryId">
                                    <option
                                        v-for="category in categories"
                                        :key="category.id"
                                        :value="category.id"
                                    >
                                        {{ category.name_en }}
                                    </option>
                                </select>
                                <v-btn
                                    color="primary"
                                    block
                                    @click="updateTagCategoryIds()"
                                >
                                    更新
                                </v-btn>
                            </v-card-text>
                        </v-card>
                    </v-dialog>
                </v-container>
            </v-table>
            <v-container class="tag-info">
                <v-container class="top-button-area">
                    <v-btn color="secondary" @click="selectedId = -1">
                        新規作成
                    </v-btn>
                </v-container>
                <v-list elevation="2">
                    <v-list-item title="id">
                        <v-list-item-subtitle class="content">
                            {{ selectedTag.id ?? '-' }}
                        </v-list-item-subtitle>
                    </v-list-item>
                    <v-list-item title="カテゴリー">
                        <select v-model="selectedTag.category_id">
                            <option
                                v-for="category in categories"
                                :key="category.id"
                                :value="category.id"
                            >
                                {{ category.name_en }}
                            </option>
                        </select>
                    </v-list-item>
                    <v-list-item title="英名">
                        <v-list-item-subtitle class="content">
                            {{ selectedTag.name_en ?? '-' }}
                        </v-list-item-subtitle>
                    </v-list-item>
                    <v-list-item title="日本語名">
                        <v-text-field
                            v-model="selectedTag.name_ja"
                            :value="selectedTag.name_ja"
                            variant="underlined"
                            hide-details
                        ></v-text-field>
                    </v-list-item>
                    <v-list-item title="キーワード">
                        <p
                            class="content"
                            v-for="word in selectedTag.words"
                            :key="word.id"
                        >
                            {{ word.name_en }}
                        </p>
                    </v-list-item>
                    <v-list-item title="最終更新日時">
                        <v-list-item-subtitle class="content">
                            {{ selectedTag.updated_at ?? '-' }}
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
