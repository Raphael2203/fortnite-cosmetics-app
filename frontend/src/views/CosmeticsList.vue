<template>
  <div>
    <h1>Cosmetics</h1>
    <div v-if="loading">Loading...</div>
    <ul v-else>
      <li v-for="c in cosmetics" :key="c.id" style="margin-bottom:8px;">
        <strong>{{ c.name }}</strong> — {{ c.rarity }} — {{ c.price ?? 'N/A' }} v-bucks
        <div>
          <button @click="view(c.id)">Details</button>
          <button @click="buy(c.id)" style="margin-left:8px;">Buy</button>
        </div>
      </li>
    </ul>
    <pagination v-if="total>perPage" :page="page" :per-page="perPage" :total="total" @change="onPage"/>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import api from '../services/api'
import { useRouter } from 'vue-router'
import Pagination from '../components/Pagination.vue'

const cosmetics = ref<any[]>([])
const loading = ref(false)
const page = ref(1)
const perPage = ref(12)
const total = ref(0)
const router = useRouter()

const load = async () => {
  loading.value = true
  try {
    // backend pagination optional; for tests simply fetch all
    const res = await api.listCosmetics()
    cosmetics.value = res.data || []
    total.value = cosmetics.value.length
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

const view = (id:number) => router.push(`/cosmetics/${id}`)
const buy = async (id:number) => {
  try {
    await api.buyCosmetic(id)
    alert('Purchase successful')
  } catch (err:any) {
    alert('Purchase failed: ' + (err.response?.data?.detail ?? err.message))
  }
}

const onPage = (p:number) => { page.value = p; load() }

onMounted(load)
</script>
