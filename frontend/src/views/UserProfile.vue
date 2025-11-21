<template>
  <div>
    <h1>User Profile</h1>
    <div v-if="loading">Loading...</div>
    <div v-else-if="profile">
      <p><strong>Email:</strong> {{ profile.email }}</p>
      <h3>Acquired Cosmetics</h3>
      <ul>
        <li v-for="c in profile.acquired_cosmetics" :key="c.id">
          {{ c.name }} — {{ c.price ?? 'N/A' }} v-bucks
        </li>
      </ul>
    </div>
    <div v-else>
      Not found
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import api from '../services/api'

const route = useRoute()
const profile = ref<any>(null)
const loading = ref(false)

const load = async () => {
  loading.value = true
  try {
    const res = await api.getUser(Number(route.params.id))
    profile.value = res.data
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

onMounted(load)
</script>
