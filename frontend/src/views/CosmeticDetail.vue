<template>
  <div>
    <h1>Cosmetic Detail</h1>
    <div v-if="!cosmetic">Loading...</div>
    <div v-else style="text-align:left;">
      <h2>{{ cosmetic.name }} <span v-if="cosmetic.is_new">🆕</span> <span v-if="cosmetic.is_on_sale">🔥</span></h2>
      <p>Rarity: {{ cosmetic.rarity }}</p>
      <p>Price: {{ cosmetic.price ?? 'N/A' }} v-bucks</p>
      <div style="margin-top:12px;">
        <button @click="buy">Buy</button>
        <button @click="ret" style="margin-left:8px;">Return</button>
        <button @click="goBack" style="margin-left:8px;">Return to list</button>
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
    alert('Bought!')
    await load()
  } catch (err:any) {
    alert('Error: ' + (err.response?.data?.detail ?? err.message))
  }
}
const ret = async () => {
  try {
    await api.returnCosmetic(Number(route.params.id))
    alert('Returned!')
    await load()
  } catch (err:any) {
    alert('Error: ' + (err.response?.data?.detail ?? err.message))
  }
}

const goBack = () => router.push('/')

onMounted(load)
</script>
