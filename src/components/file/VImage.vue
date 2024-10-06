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
    <v-card>
        <v-img
            @click="select(props.index)"
            class="bg-grey-lighten-3 img-content"
            max-height="280"
            :src="
                props.image.imported_path !== undefined
                    ? props.image.imported_path
                    : props.image.path
            "
            :alt="props.image.name"
            cover
        ></v-img>
        <v-card-title class="img-text">{{ props.image.name }}</v-card-title>
    </v-card>
</template>
