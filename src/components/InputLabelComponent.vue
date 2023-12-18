<script setup>
import { defineProps } from 'vue'
import '@/assets/scss/style.scss'

const props = defineProps(['text', 'idName', 'type'])
const inputType = props.type || 'text'
</script>
<template>
    <div>
        <input :id="idName" :type="inputType" />
        <label :for="idName">{{ text }}</label>
    </div>
</template>
