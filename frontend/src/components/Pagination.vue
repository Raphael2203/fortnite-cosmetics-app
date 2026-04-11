<template>
  <div class="pagination-container">
    <button class="btn-pagination" :disabled="page <= 1" @click="$emit('change', page - 1)">
      &laquo; Prev
    </button>
    
    <span class="page-indicator">Page {{ page }} of {{ last }}</span>
    
    <button class="btn-pagination" :disabled="page >= last" @click="$emit('change', page + 1)">
      Next &raquo;
    </button>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
const props = defineProps({
  page: { type: Number, required: true },
  perPage: { type: Number, required: true },
  total: { type: Number, required: true }
})
const last = computed(() => Math.max(1, Math.ceil(props.total / props.perPage)))
</script>
