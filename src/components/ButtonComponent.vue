<script setup>
import { defineProps } from 'vue'
import '@/assets/scss/style.scss'

const props = defineProps(['text', 'buttonClass', 'handleClick'])
</script>
<template>
    <button @click="handleClick" :class="buttonClass">
        {{ text }}
    </button>
</template>
