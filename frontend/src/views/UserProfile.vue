<template>
  <div style="max-width: 800px; margin: 0 auto; padding: 20px;">
    <h1 style="color: #fdf035; text-transform: uppercase; font-style: italic;">User Profile</h1>
    
    <div v-if="loading" style="text-align: center; padding: 40px;">
      <div class="skeleton" style="height: 30px; width: 200px; margin: 0 auto 20px;"></div>
      <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(150px, 1fr)); gap: 15px;">
        <div v-for="n in 4" :key="n" class="skeleton" style="height: 180px; border-radius: 8px;"></div>
      </div>
    </div>

    <div v-else-if="profile">
      <div style="background: #1a1a1a; padding: 20px; border-radius: 12px; border: 1px solid #333; margin-bottom: 30px; display: flex; justify-content: space-between; align-items: center;">
        <div>
          <p style="margin: 0; color: #888; font-size: 0.9rem; text-transform: uppercase;">Account Email</p>
          <strong style="font-size: 1.2rem; color: #fff;">{{ profile.email }}</strong>
        </div>
        <div style="text-align: right;">
          <p style="margin: 0; color: #888; font-size: 0.9rem; text-transform: uppercase;">Current Balance</p>
          <div style="display: flex; align-items: center; gap: 8px; justify-content: flex-end;">
            <img src="https://fortnite-api.com/images/vbuck.png" width="20" />
            <span style="font-size: 1.4rem; color: #ffd700; font-weight: bold;">{{ profile.vbucks ?? 0 }}</span>
          </div>
        </div>
      </div>

      <h3 style="border-bottom: 2px solid #8b31ff; padding-bottom: 8px; margin-bottom: 20px;">Acquired Cosmetics</h3>
      
      <div v-if="profile.acquired_cosmetics?.length" style="display: grid; grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap: 20px;">
        <div v-for="c in profile.acquired_cosmetics" :key="c.id" 
             style="background: #1e1e2f; border-radius: 8px; overflow: hidden; border: 1px solid #444; text-align: center; transition: 0.3s;"
             class="cosmetic-card">
          
          <img :src="c.image_url || 'https://fortnite-api.com/images/placeholder.png'" 
               style="width: 100%; height: 140px; object-fit: contain; background: #2a2a3c; border-bottom: 1px solid #333;" />
          
          <div style="padding: 10px;">
            <div style="font-weight: bold; font-size: 0.9rem; color: #eee; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">
              {{ c.name }}
            </div>
            <div style="color: #8b31ff; font-size: 0.75rem; font-weight: bold; text-transform: uppercase; margin-top: 4px;">
              {{ c.rarity }}
            </div>
          </div>
        </div>
      </div>
      
      <div v-else style="background: #1a1a1a; padding: 40px; text-align: center; border-radius: 8px; color: #666; border: 1px dashed #444;">
        This user hasn't acquired any cosmetics yet.
      </div>

      <div style="margin-top: 30px; text-align: center;">
        <button @click="$router.push('/users')" style="background: transparent; color: #888; border: 1px solid #444; padding: 8px 16px; border-radius: 6px; cursor: pointer;">
          &larr; Back to Users List
        </button>
      </div>
    </div>

    <div v-else style="text-align: center; padding: 50px;">
      <h2 style="color: #ff4444;">User Not Found</h2>
      <button @click="$router.push('/')">Return to Shop</button>
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

<style scoped>
.cosmetic-card:hover {
  transform: translateY(-5px);
  border-color: #8b31ff;
  box-shadow: 0 5px 15px rgba(139, 49, 255, 0.2);
}
</style>