<template>
  <div>
    <h1>Users</h1>
    <div v-if="loading">Loading...</div>
    <ul v-else>
      <li v-for="u in users" :key="u.id">
        <a @click.prevent="view(u.id)" href="#">{{ u.email }}</a>
      </li>
    </ul>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import api from '../services/api'
import { useRouter } from 'vue-router'

const users = ref<any[]>([])
const loading = ref(false)
const router = useRouter()

const load = async () => {
  loading.value = true
  try {
    const res = await api.listUsers()
    users.value = res.data || []
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}
const view = (id:number) => router.push(`/users/${id}`)

onMounted(load)
</script>
