<template>
  <nav style="padding:12px; border-bottom:1px solid #eee; display:flex; align-items:center; justify-content:space-between;">
    <div>
      <router-link to="/">Cosmetics</router-link> |
      <router-link to="/users">Users</router-link>
    </div>
    <div>
      <template v-if="currentUser">
        <span style="margin-right:12px;">{{ currentUser.email }}</span>
        <button @click="showHistory = !showHistory">History</button>
        <button @click="logout" style="margin-left:8px;">Logout</button>
      </template>
      <template v-else>
        <button @click="showLogin = true">Login</button>
        <button @click="showRegister = true" style="margin-left:8px;">Register</button>
      </template>
    </div>
  </nav>

  <main style="padding:16px;">
    <router-view />
  </main>

  <!-- Login Modal (dark) -->
  <div v-if="showLogin" class="modal-overlay">
    <div class="modal">
      <h3>Login</h3>
      <input v-model="loginForm.email" placeholder="email" class="input" />
      <input v-model="loginForm.password" type="password" placeholder="password" class="input" />
      <div class="modal-actions">
        <button @click="doLogin">Login</button>
        <button @click="showLogin = false" class="secondary">Close</button>
      </div>
      <div v-if="authError" class="error">{{ authError }}</div>
    </div>
  </div>

  <!-- Register Modal (dark) -->
  <div v-if="showRegister" class="modal-overlay">
    <div class="modal">
      <h3>Register</h3>
      <input v-model="regForm.email" placeholder="email" class="input" />
      <input v-model="regForm.password" type="password" placeholder="password" class="input" />
      <div class="modal-actions">
        <button @click="doRegister">Register</button>
        <button @click="showRegister = false" class="secondary">Close</button>
      </div>
      <div v-if="authError" class="error">{{ authError }}</div>
    </div>
  </div>

  <!-- History drawer -->
  <div v-if="showHistory" style="position:fixed; right:0; top:0; height:100%; width:380px; background:#111; color:#eee; border-left:1px solid #333; padding:16px; overflow:auto;">
    <h3>Purchase History</h3>
    <div v-if="historyLoading">Loading...</div>
    <ul v-else>
      <li v-for="h in history" :key="h.id" style="margin-bottom:8px;">
        <div><strong>Type:</strong> {{ h.type }}</div>
        <div v-if="h.cosmetic">Cosmetic: {{ h.cosmetic.name }}</div>
        <div><small>{{ h.created_at }}</small></div>
      </li>
    </ul>
    <div style="text-align:right;"><button @click="showHistory=false">Close</button></div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import api from './services/api'

const currentUser = ref<any>(null)
const showLogin = ref(false)
const showRegister = ref(false)
const showHistory = ref(false)
const authError = ref<string | null>(null)

const loginForm = ref({ email: '', password: '' })
const regForm = ref({ email: '', password: '' })

const history = ref<any[]>([])
const historyLoading = ref(false)

const loadMe = async () => {
  try {
    const res = await api.me()
    currentUser.value = res.data
  } catch (e) {
    currentUser.value = null
  }
}

const doLogin = async () => {
  authError.value = null
  try {
    const res = await api.login({ ...loginForm.value })
    const token = res.data.access_token
    api.setToken(token)
    await loadMe()
    showLogin.value = false
    loginForm.value = { email: '', password: '' }
  } catch (err:any) {
    authError.value = err.response?.data?.detail ?? err.message
  }
}

const doRegister = async () => {
  authError.value = null
  try {
    await api.register({ ...regForm.value })
    const res = await api.login({ ...regForm.value })
    const token = res.data.access_token
    api.setToken(token)
    await loadMe()
    showRegister.value = false
    regForm.value = { email: '', password: '' }
  } catch (err:any) {
    authError.value = err.response?.data?.detail ?? err.message
  }
}

const logout = () => {
  api.clearToken()
  currentUser.value = null
}

const loadHistory = async () => {
  if (!currentUser.value) return
  historyLoading.value = true
  try {
    const res = await api.history()
    history.value = res.data || []
  } catch (e) {
    history.value = []
  } finally {
    historyLoading.value = false
  }
}

onMounted(async () => {
  // initialize user if token present
  await loadMe()
})

// watch showHistory open
watch(showHistory, (v) => { if (v) loadHistory() })
</script>

<style scoped>
/* dark modal + inputs */
.modal-overlay {
  position: fixed;
  inset: 0;
  display: grid;
  place-items: center;
  background: rgba(0,0,0,0.6);
  z-index: 60;
}
.modal {
  background: #0f1720;
  color: #e6eef8;
  padding: 18px;
  border-radius: 10px;
  min-width: 320px;
  box-shadow: 0 10px 30px rgba(0,0,0,0.6);
  border: 1px solid rgba(255,255,255,0.03);
}
.input {
  width: 100%;
  padding: 10px 12px;
  margin-bottom: 8px;
  background: #0b1220;
  border: 1px solid rgba(255,255,255,0.06);
  color: #e6eef8;
  border-radius: 6px;
}
.input::placeholder {
  color: #99a3b2;
}
.modal-actions {
  display:flex;
  justify-content:flex-end;
  gap:8px;
  margin-top:8px;
}
button {
  background: #0b1220;
  color: #e6eef8;
  border: 1px solid rgba(255,255,255,0.06);
  padding: 8px 12px;
  border-radius: 8px;
}
button.secondary {
  background: transparent;
  border: 1px solid rgba(255,255,255,0.04);
}
.error {
  color: #ff6b6b;
  margin-top:8px;
}
</style>
