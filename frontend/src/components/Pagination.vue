<template>
  <div style="margin-top:12px;">
    <button :disabled="page<=1" @click="$emit('change', page-1)">Prev</button>
    <span style="margin:0 8px;">Page {{ page }}</span>
    <button :disabled="page>=last" @click="$emit('change', page+1)">Next</button>
  </div>
</template>

<script setup lang="ts">
import { defineProps } from 'vue'
const props = defineProps({
  page: { type: Number, required: true },
  perPage: { type: Number, required: true },
  total: { type: Number, required: true }
})
const last = Math.max(1, Math.ceil(props.total / props.perPage))
</script>
