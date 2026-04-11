<template>
  <div style="max-width: 900px; margin: 0 auto; padding: 20px;">
    <h1 style="color: #fdf035; text-transform: uppercase; font-style: italic;">Cosmetic Detail</h1>
    
    <div v-if="!cosmetic" style="text-align: center; padding: 50px;">
      <div class="skeleton" style="height: 300px; width: 100%; border-radius: 12px;"></div>
    </div>

    <div v-else style="display: flex; gap: 40px; align-items: flex-start; background: #1a1a1a; padding: 30px; border-radius: 12px; border: 1px solid #333; flex-wrap: wrap;">
      
      <div style="flex: 1; min-width: 300px;">
        <img 
          :src="cosmetic.image_url || 'https://fortnite-api.com/images/placeholder.png'" 
          :alt="cosmetic.name"
          style="width: 100%; height: auto; border-radius: 8px; background: #252525; border: 2px solid #8b31ff; box-shadow: 0 0 20px rgba(139, 49, 255, 0.2);"
        />
      </div>

      <div style="flex: 1; min-width: 300px; text-align: left;">
        <h2 style="font-size: 2.5rem; margin: 0 0 10px 0; color: white;">
          {{ cosmetic.name }} 
          <span v-if="cosmetic.is_new" title="New Item">🆕</span> 
          <span v-if="cosmetic.is_on_sale" title="On Sale">🔥</span>
        </h2>

        <p style="font-size: 1.2rem; margin-bottom: 20px;">
          Rarity: <span :style="{ color: getRarityColor(cosmetic.rarity), fontWeight: 'bold', textTransform: 'uppercase' }">
            {{ cosmetic.rarity }}
          </span>
        </p>

        <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 30px; background: #222; padding: 10px 20px; border-radius: 8px; width: fit-content;">
          <img src="https://fortnite-api.com/images/vbuck.png" width="30" />
          <span style="font-size: 1.8rem; color: #ffd700; font-weight: bold;">{{ cosmetic.price ?? 'N/A' }}</span>
        </div>

        <div style="display: flex; flex-direction: column; gap: 12px;">
          <button @click="buy" class="btn-buy-large">PURCHASE ITEM</button>
          
          <div style="display: flex; gap: 10px;">
            <button @click="ret" class="btn-return">RETURN ITEM</button>
            <button @click="goBack" class="btn-back">BACK TO LIST</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '../services/api'

const route = useRoute()
const router = useRouter()
const cosmetic = ref<any>(null)

const getRarityColor = (rarity: string) => {
  const r = rarity?.toLowerCase()
  if (r.includes('legendary') || r.includes('lendário')) return '#d37841'
  if (r.includes('epic') || r.includes('épico')) return '#b052fb'
  if (r.includes('rare') || r.includes('raro')) return '#2196f3'
  if (r.includes('uncommon') || r.includes('incomum')) return '#4caf50'
  return '#eee'
}

const load = async () => {
  try {
    const res = await api.getCosmetic(Number(route.params.id))
    cosmetic.value = res.data
  } catch (e) {
    console.error(e)
  }
}

const buy = async () => {
  try {
    await api.buyCosmetic(Number(route.params.id))
    alert('Purchased successfully!')
    await load()
  } catch (err: any) {
    alert('Error: ' + (err.response?.data?.detail ?? err.message))
  }
}

const ret = async () => {
  try {
    await api.returnCosmetic(Number(route.params.id))
    alert('Item returned!')
    await load()
  } catch (err: any) {
    alert('Error: ' + (err.response?.data?.detail ?? err.message))
  }
}

const goBack = () => router.push('/')

onMounted(load)
</script>

<style scoped>
.btn-buy-large {
  background: #007bff;
  color: white;
  padding: 18px;
  border: none;
  border-radius: 6px;
  font-weight: bold;
  font-size: 1.1rem;
  cursor: pointer;
  transition: 0.2s;
}
.btn-buy-large:hover { background: #0056b3; transform: scale(1.02); }

.btn-return {
  flex: 1;
  background: #dc3545;
  color: white;
  padding: 12px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}

.btn-back {
  flex: 1;
  background: #444;
  color: white;
  padding: 12px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}

.skeleton {
  background: #222;
  animation: pulse 1.5s infinite;
}
@keyframes pulse {
  0% { opacity: 1; }
  50% { opacity: 0.5; }
  100% { opacity: 1; }
}
</style>