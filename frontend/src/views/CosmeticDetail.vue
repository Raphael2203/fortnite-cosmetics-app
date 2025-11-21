<template>
  <div>
    <h1>Cosmetic Detail</h1>
    <div v-if="!cosmetic">Loading...</div>
    <div v-else>
      <h2>{{ cosmetic.name }}</h2>
      <p>Rarity: {{ cosmetic.rarity }}</p>
      <p>Price: {{ cosmetic.price ?? 'N/A' }} v-bucks</p>
      <button @click="buy">Buy</button>
      <button @click="ret" style="margin-left:8px;">Return</button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import api from '../services/api'

const route = useRoute()
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
  } catch (err:any) {
    alert('Error: ' + (err.response?.data?.detail ?? err.message))
  }
}
const ret = async () => {
  try {
    await api.returnCosmetic(Number(route.params.id))
    alert('Returned!')
  } catch (err:any) {
    alert('Error: ' + (err.response?.data?.detail ?? err.message))
  }
}

onMounted(load)
</script>
