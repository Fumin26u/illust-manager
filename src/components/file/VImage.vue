<script setup lang="ts">
import { defineProps, defineEmits } from 'vue'
import { Image } from '@/types/image'

const props = defineProps<{
    image: Image
    index: number
}>()
const emits = defineEmits(['select'])
const select = (index: number) => emits('select', index)
</script>

<template>
    <div>
        <dt>{{ props.image.name }}</dt>
        <dd @click="select(props.index)">
            <img
                :src="
                    props.image.imported_path !== undefined
                        ? props.image.imported_path
                        : props.image.path
                "
                :alt="props.image.name"
            />
        </dd>
    </div>
</template>
