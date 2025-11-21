<template>
  <div>
    <h1>Cosmetics</h1>

    <div style="margin-bottom:12px; display:flex; gap:8px; align-items:center; justify-content:center;">
      <input v-model="filters.name" placeholder="Search name" style="padding:8px; width:240px;" />
      <select v-model="filters.rarity" style="padding:8px;">
        <option value="">All rarities</option>
        <option value="legendary">legendary</option>
        <option value="rare">rare</option>
        <option value="uncommon">uncommon</option>
        <option value="comum">comum</option>
      </select>
      <label><input type="checkbox" v-model="filters.is_new" /> New 🆕</label>
      <label><input type="checkbox" v-model="filters.is_on_sale" /> On Sale 🔥</label>
      <button @click="onSearch">Search</button>
    </div>

    <div v-if="loading">Loading...</div>
    <ul v-else>
      <li v-for="c in cosmetics" :key="c.id" style="margin-bottom:12px; text-align:left;">
        <div style="display:flex; align-items:center; justify-content:space-between;">
          <div>
            <strong>{{ c.name }}</strong>
            <small style="margin-left:8px;color:#666">{{ c.rarity }}</small>
            <div style="font-size:0.9em;color:#888;">{{ c.price ?? 'N/A' }} v-bucks</div>
            <div style="margin-top:6px;">
              <span v-if="c.is_new" title="New">🆕</span>
              <span v-if="c.is_on_sale" title="On Sale" style="margin-left:8px;">🔥</span>
            </div>
          </div>
          <div>
            <button @click="view(c.id)">Details</button>
            <button @click="buy(c.id)" style="margin-left:8px;">Buy</button>
          </div>
        </div>
      </li>
    </ul>
    <pagination v-if="total>perPage" :page="page" :per-page="perPage" :total="total" @change="onPage"/>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import api from '../services/api'
import { useRouter } from 'vue-router'
import Pagination from '../components/Pagination.vue'

const cosmetics = ref<any[]>([])
const loading = ref(false)
const page = ref(1)
const perPage = ref(12)
const total = ref(0)
const router = useRouter()

const filters = ref({
  name: '',
  rarity: '',
  is_new: false as boolean | null,
  is_on_sale: false as boolean | null
})

const load = async () => {
  loading.value = true
  try {
    const params: any = { page: page.value, size: perPage.value }
    if (filters.value.name) params.name = filters.value.name
    if (filters.value.rarity) params.rarity = filters.value.rarity
    if (filters.value.is_new) params.is_new = true
    if (filters.value.is_on_sale) params.is_on_sale = true

    const res = await api.listCosmetics(params)
    cosmetics.value = res.data?.items ? res.data.items : (res.data || [])
    total.value = res.data?.total ?? cosmetics.value.length
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
    load()
  } catch (err:any) {
    alert('Purchase failed: ' + (err.response?.data?.detail ?? err.message))
  }
}

const onPage = (p:number) => { page.value = p; load() }
const onSearch = () => { page.value = 1; load() }

load()
</script>
