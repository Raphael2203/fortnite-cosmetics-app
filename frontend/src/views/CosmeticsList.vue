<template>
  <div>
    <h1>Welcome to the Fortnite Shop!</h1>
    
    <div style="margin-bottom:20px; display:flex; gap:8px; align-items:center; justify-content:center; flex-wrap: wrap; background: #1a1a1a; padding: 15px; border-radius: 8px;">
      <input v-model="filters.name" placeholder="Search name" style="padding:10px; width:240px; background: #333; border: 1px solid #444; color: white; border-radius: 4px;" />
      <select v-model="filters.rarity" style="padding:10px; background: #333; border: 1px solid #444; color: white; border-radius: 4px;">
        <option value="">All rarities</option>
        <option v-for="rarity in dynamicRarities" :key="rarity" :value="rarity"> {{ rarity }}</option>
      </select>
      <label style="color: #eee; cursor: pointer;"><input type="checkbox" v-model="filters.is_new" /> New 🆕</label>
      <label style="color: #eee; cursor: pointer;"><input type="checkbox" v-model="filters.is_on_sale" /> On Sale 🔥</label>
      <button @click="onSearch" style="padding: 10px 20px; background: #8b31ff; border: none; color: white; border-radius: 4px; cursor: pointer; font-weight: bold;">Search</button>
    </div>

    <div v-if="loading" class="loading-state">
      <div class="spinner"></div>
      <p>Sincronizando com o servidor...</p>
      <small v-if="showSlowMessage">O banco de dados está sendo iniciado, aguarde um instante.</small>
      <div v-for="n in 6" :key="n" style="margin-bottom:20px; display:flex; justify-content:space-between; align-items:center; background: #1a1a1a; padding: 15px; border-radius: 8px;">
        <div style="display: flex; align-items: center; gap: 15px; width: 60%;">
          <div class="skeleton" style="height: 50px; width: 50px; border-radius: 4px;"></div>
          <div style="flex-grow: 1;">
            <div class="skeleton" style="height: 20px; width: 60%; margin-bottom: 8px;"></div>
            <div class="skeleton" style="height: 15px; width: 30%;"></div>
          </div>
        </div>
        <div class="skeleton" style="height: 35px; width: 100px; border-radius: 4px;"></div>
      </div>
    </div>

    <ul v-else style="list-style: none; padding: 0;">
      <li v-for="c in cosmetics" :key="c.id" style="margin-bottom:12px; background: #1a1a1a; padding: 12px; border-radius: 8px; border: 1px solid #333; transition: 0.2s;">
        <div style="display:flex; align-items:center; justify-content:space-between;">
          <div style="display: flex; align-items: center; gap: 15px;">
            <img 
              :src="c.image_url || 'https://fortnite-api.com/images/placeholder.png'" 
              style="width: 55px; height: 55px; border-radius: 4px; background: #252525; object-fit: contain; border: 1px solid #444;"
            />
            
            <div>
              <strong style="font-size: 1.1rem; color: #fff;">{{ c.name }}</strong>
              <small style="margin-left:8px; color:#8b31ff; font-weight: bold; text-transform: uppercase;">{{ c.rarity }}</small>
              <div style="font-size:0.95em; color:#ffd700; display: flex; align-items: center; gap: 4px; margin-top: 2px;">
                <img src="https://fortnite-api.com/images/vbuck.png" width="14" />
                {{ c.price ?? 'N/A' }}
              </div>
              <div style="margin-top:6px;">
                <span v-if="c.is_new" title="New" style="font-size: 0.8rem; background: #28a745; padding: 2px 6px; border-radius: 4px; color: white;">NEW</span>
                <span v-if="c.is_on_sale" title="On Sale" style="margin-left:8px; font-size: 0.8rem; background: #dc3545; padding: 2px 6px; border-radius: 4px; color: white;">SALE</span>
              </div>
            </div>
          </div>

          <div style="display: flex; gap: 10px;">
            <button @click="view(c.id)" style="background: #444; color: white; padding: 8px 16px; border: none; border-radius: 4px; cursor: pointer;">Details</button>
            <button @click="buy(c.id)" style="background: #007bff; color: white; padding: 8px 16px; border: none; border-radius: 4px; cursor: pointer; font-weight: bold;">Buy</button>
          </div>
        </div>
      </li>
    </ul>

    <pagination v-if="total > perPage" :page="page" :per-page="perPage" :total="total" @change="onPage"/>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import api from '../services/api'
import { useRouter } from 'vue-router'
import Pagination from '../components/Pagination.vue'

const cosmetics = ref<any[]>([])
const loading = ref(false)
const page = ref(1)
const perPage = ref(12)
const total = ref(0)
const router = useRouter()
const userVBucks = ref(0)
const username = ref('')
const showSlowMessage = ref(false)

const filters = ref({
  name: '',
  rarity: '',
  is_new: false as boolean | null,
  is_on_sale: true
})

const load = async () => {
  loading.value = true
  showSlowMessage.value = false

  const slowTimer = setTimeout(() => {
    if (loading.value) showSlowMessage.value = true
  }, 4000)

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
    console.error("Erro definitivo após retries:", e)
  } finally {
    clearTimeout(slowTimer)
    loading.value = false
  }
}
const loadUser = async () => {
  try {
    const res = await api.me()
    userVBucks.value = res.data.vbucks
    username.value = res.data.username
  } catch (e: any) {
    if (e.response?.status === 401) return 
    console.error("Erro ao carregar saldo:", e)
  }
}

const view = (id: number) => router.push(`/cosmetics/${id}`)
const buy = async (id: number) => {
  try {
    await api.buyCosmetic(id)
    alert('Purchase successful!')
    await loadUser()
    load()
  } catch (err: any) {
    alert('Purchase failed: ' + (err.response?.data?.detail ?? err.message))
  }
}

const dynamicRarities = computed(() => {
  const allRarities = cosmetics.value.map(c => c.rarity).filter(Boolean);
  return [...new Set(allRarities)].sort();
})

const onPage = (p: number) => { page.value = p; load() }
const onSearch = () => { page.value = 1; load() }

onMounted(() => {
  load();
  const token = localStorage.getItem("fc_token");
  if (token) {
    loadUser();
  }
});
</script>