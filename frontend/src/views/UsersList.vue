<template>
  <div style="max-width: 900px; margin: 0 auto; padding: 20px;">
    <h1 style="color: #fdf035; text-transform: uppercase; font-style: italic; margin-bottom: 25px;">Registered Users</h1>
    
    <div v-if="loading" style="text-align: center; padding: 40px;">
      <div v-for="n in 5" :key="n" class="skeleton" style="height: 60px; margin-bottom: 10px; border-radius: 8px;"></div>
    </div>

    <div v-else-if="users.length" style="background: #1a1a1a; border-radius: 12px; border: 1px solid #333; overflow: hidden;">
      <table style="width: 100%; border-collapse: collapse; text-align: left; color: #eee;">
        <thead>
          <tr style="background: #2a2a2a; color: #888; text-transform: uppercase; font-size: 0.8rem;">
            <th style="padding: 15px;">User Email</th>
            <th style="padding: 15px; text-align: center;">Balance</th>
            <th style="padding: 15px; text-align: right;">Action</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="u in users" :key="u.id" class="user-row" style="border-bottom: 1px solid #333;">
            <td style="padding: 15px;">
              <div style="display: flex; align-items: center; gap: 10px;">
                <div style="width: 35px; height: 35px; background: #8b31ff; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold; color: white;">
                  {{ u.email[0].toUpperCase() }}
                </div>
                <strong>{{ u.email }}</strong>
              </div>
            </td>
            <td style="padding: 15px; text-align: center;">
              <div style="display: inline-flex; align-items: center; gap: 6px; background: #222; padding: 4px 10px; border-radius: 15px; border: 1px solid #444;">
                <img src="https://fortnite-api.com/images/vbuck.png" width="16" />
                <span style="color: #ffd700; font-weight: bold;">{{ u.vbucks ?? 0 }}</span>
              </div>
            </td>
            <td style="padding: 15px; text-align: right;">
              <button @click="view(u.id)" class="btn-view">
                View Profile
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-else style="text-align: center; padding: 50px; color: #666;">
      <p>No users found in the database.</p>
    </div>
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
    // O backend agora retorna o campo vbucks no UserOut
    users.value = res.data || []
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

const view = (id: number) => router.push(`/users/${id}`)

onMounted(load)
</script>

<style scoped>
.user-row:hover {
  background: #252525;
}

.btn-view {
  background: transparent;
  color: #42b983;
  border: 1px solid #42b983;
  padding: 6px 12px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.85rem;
  transition: 0.2s;
}

.btn-view:hover {
  background: #42b983;
  color: #111;
}

.skeleton {
  background: linear-gradient(90deg, #222 25%, #333 50%, #222 75%);
  background-size: 200% 100%;
  animation: loading 1.5s infinite;
}

@keyframes loading {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}
</style>