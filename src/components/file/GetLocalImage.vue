<script setup lang="ts">
import { ref, defineProps, defineEmits } from 'vue'

const props = defineProps(['title'])
const emits = defineEmits(['setImageInfo'])

const directoryPath = ref<string | null>(null)
</script>

<template>
    <div>
        <dt>{{ title }}</dt>
        <dd>
            <input type="file" webkitdirectory @change="" />
            <p v-if="directoryPath !== null">{{ directoryPath }}</p>
        </dd>
    </div>
</template>
