<script setup lang="ts">
import { ref, defineProps, defineEmits } from 'vue'
import { ImageInfo } from '@/types'

const props = defineProps(['title'])
const emits = defineEmits(['setImageInfo'])

const directoryPath = ref<string | null>(null)

// 指定されたディレクトリ内の画像ファイルから画像リンク一覧を取得
const selectFile = (event: Event) => {
    const input = event.target as HTMLInputElement
    const files = input.files
    // console.log(files[0].webkitRelativePath.split('/'))

    // バリデーション
    if (!files) return 'ファイルが選択されていません。'
    if (files.length === 0) return 'ファイルが空です。'

    const imageInfo: ImageInfo[] = Array.from(files).map((file, index) => ({
        rawPath: file.name,
        imagePath: URL.createObjectURL(file),
        childDir: file.webkitRelativePath.split('/')[1],
        className: '',
        confidence: '',
        isImportant: false,
        index: index,
    }))

    // 親コンポーネントに画像情報一覧を渡す
    emits('setImageInfo', imageInfo)
}
</script>

<template>
    <div>
        <dt>{{ title }}</dt>
        <dd>
            <input type="file" webkitdirectory @change="selectFile" />
            <p v-if="directoryPath !== null">{{ directoryPath }}</p>
        </dd>
    </div>
</template>
