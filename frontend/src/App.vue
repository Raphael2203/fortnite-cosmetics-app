<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import api from './services/api'

const isDBReady = ref(false)
const retryCount = ref(0)
const currentUser = ref<any>(null)
const showLogin = ref(false)
const showRegister = ref(false)
const showHistory = ref(false)
const authError = ref<string | null>(null)
const loginForm = ref({ email: '', password: '' })
const regForm = ref({ email: '', password: '' })
const history = ref<any[]>([])
const historyLoading = ref(false)

const wakeUpDataBase = async () => {
  try {
    await api.checkHealth()
    isDBReady.value = true
  } catch(err) {
    retryCount.value++
    setTimeout(wakeUpDataBase, 2000)
  }
}

const loadMe = async () => {
  try {
    const res = await api.me()
    currentUser.value = res.data
  } catch (e: any) {
    if (e.response?.status === 401) {
    currentUser.value = null;
    return;
  }
  console.error("Erro inesperado ao carregar usuário:", e);
  }
}

const sellItem = async (cosmeticId: number) => {
  if (!confirm("Deseja devolver este item? Os V-Bucks serão estornados.")) return

  try {
    await api.returnCosmetic(cosmeticId)
    history.value = history.value.filter(h => !(h.type === 'buy' && h.cosmetic?.id === cosmeticId))
    await loadMe()
    await loadHistory()
    
    alert("Item devolvido com sucesso!")
  } catch (err: any) {
    alert("Erro ao devolver item: " + (err.response?.data?.detail ?? err.message))
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
  } catch (err: any) {
    authError.value = err.response?.data?.detail ?? err.message
  }
}

const fillTestAccount = () => {
  loginForm.value.email = 'admin@admin.com'
  loginForm.value.password = 'admin123'
  doLogin()
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
  } catch (err: any) {
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

const activeTab = ref<'comprados' | 'vendidos'>('comprados')
import { computed } from 'vue'

const filteredHistory = computed(() => {
  const returnedIds = history.value
    .filter(h => h.type === 'return')
    .map(h => h.cosmetic?.id);

  if (activeTab.value === 'comprados') {
    return history.value.filter(h => 
      h.type === 'buy' && 
      h.cosmetic && 
      !returnedIds.includes(h.cosmetic.id)
    );
  } else {
    return history.value.filter(h => h.type === 'return');
  }
})

onMounted(async () => {
  await wakeUpDataBase();
  const savedToken = localStorage.getItem("fc_token");
  if (savedToken) {
    api.setToken(savedToken);
    await loadMe()
  } else {
    currentUser.value = null;
    api.setToken(null);
  }
})

watch(showHistory, (v) => { if (v) loadHistory() })
</script>

<template>
  <div v-if="!isDBReady" class="loading-overlay">
    <div class="loader-content">
      <div class="spinner"></div>
      <h2>Fortnite Cosmetics</h2>
      <p>Acordando o banco de dados... (Tentativa {{ retryCount }})</p>
      <span>Isso acontece após períodos de inatividade no Supabase.</span>
    </div>
  </div>

  <nav style="padding:12px; border-bottom:1px solid #333; display:flex; align-items:center; justify-content:space-between; background: #1a1a1a; color: white;">
    <div style="display: flex; gap: 15px; align-items: center;">
      <router-link to="/" style="text-decoration: none; color: #42b983; font-weight: bold;">Cosmetics</router-link>
      <router-link to="/users" style="text-decoration: none; color: #42b983; font-weight: bold;">Users</router-link>
    </div>

    <div style="display: flex; gap: 20px; align-items: center;">
      <a href="https://github.com/Raphael2203/fortnite-cosmetics-app" target="_blank" style="display: flex; align-items: center; gap: 5px; color: #eee; text-decoration: none;">
        <img src="/github-logo.png" width="22" alt="GitHub">
        <span style="font-size: 0.85em;">GitHub</span>
      </a>
      <a href="https://www.linkedin.com/in/raphael-brito-sa/" target="_blank" style="display: flex; align-items: center; gap: 5px; color: #eee; text-decoration: none;">
        <img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" width="22" alt="LinkedIn">
        <span style="font-size: 0.85em;">LinkedIn</span>
      </a>
    </div>

    <div style="display: flex; align-items: center; gap: 12px;">
      <template v-if="currentUser">
        <div style="display: flex; align-items: center; gap: 5px; background: #2a2a2a; padding: 4px 10px; border-radius: 20px;">
          <img src="https://fortnite-api.com/images/vbuck.png" width="18" />
          <span style="font-weight: bold; color: #ffd700;">{{ currentUser.vbucks }}</span>
        </div>
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

  <div v-if="showHistory" style="position:fixed; right:0; top:0; height:100%; width:380px; background:#111; color:#eee; border-left:2px solid #8b31ff; padding:16px; overflow:auto; z-index: 100;">
    <h3 style="color: #fdf035; font-style: italic; text-transform: uppercase; margin-bottom: 20px;">History</h3>

    <div style="display: flex; gap: 8px; margin-bottom: 20px;">
      <button 
        @click="activeTab = 'comprados'"
        :style="{
          flex: 1, padding: '8px', cursor: 'pointer', border: 'none', borderRadius: '4px',
          background: activeTab === 'comprados' ? '#8b31ff' : '#333',
          color: 'white', fontWeight: 'bold'
        }"
      >
        COMPRADOS
      </button>
      <button 
        @click="activeTab = 'vendidos'"
        :style="{
          flex: 1, padding: '8px', cursor: 'pointer', border: 'none', borderRadius: '4px',
          background: activeTab === 'vendidos' ? '#8b31ff' : '#333',
          color: 'white', fontWeight: 'bold'
        }"
      >
        VENDIDOS
      </button>
    </div>

    <div v-if="historyLoading">Loading...</div>

    <ul v-else style="list-style: none; padding: 0;">
      <li v-for="h in filteredHistory" :key="h.id" 
          :style="{
            marginBottom: '12px', padding: '12px', background: '#1e1e2f', borderRadius: '6px', 
            borderLeft: activeTab === 'comprados' ? '4px solid #007bff' : '4px solid #ff4444',
            display: 'flex', alignItems: 'center', gap: '12px'
          }">
        
        <img v-if="h.cosmetic?.image_url" :src="h.cosmetic.image_url" width="50" height="50" style="border-radius: 4px; object-fit: cover;" />
        
        <div style="flex-grow: 1;">
          <div v-if="h.cosmetic" style="color: #fff; font-weight: 600; font-size: 0.9rem;">{{ h.cosmetic.name }}</div>
          
          <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 4px;">
            <small style="color: #888; font-size: 0.7rem;">{{ new Date(h.created_at).toLocaleDateString('pt-BR') }}</small>
            
            <button 
              v-if="activeTab === 'comprados' && h.cosmetic" 
              @click="sellItem(h.cosmetic.id)"
              style="background: #ff4444; color: white; border: none; padding: 4px 6px; border-radius: 4px; cursor: pointer; font-size: 0.6rem; font-weight: bold;"
            >
              VENDER
            </button>
          </div>
        </div>
      </li>
      
      <div v-if="filteredHistory.length === 0" style="text-align: center; color: #666; margin-top: 20px;">
        Nenhum item nesta categoria.
      </div>
    </ul>

    <div style="margin-top: 20px;">
      <button @click="showHistory = false" style="width: 100%; padding: 10px; cursor: pointer; background: #222; color: #888; border: 1px solid #444;">Close</button>
    </div>
</div>

<div v-if="showLogin" class="modal-overlay">
  <div class="modal">
    <h3>Login</h3>
    <input v-model="loginForm.email" placeholder="Email" class="input" />
    <input v-model="loginForm.password" type="password" placeholder="Password" class="input" />
    
    <div class="modal-actions">
      <button @click.prevent="doLogin">Login</button>
      <button @click="showLogin = false" class="secondary">Close</button>
    </div>

    <div v-if="authError" class="error">{{ authError }}</div>

    <div class="demo-section">
      <span>Quer testar sem cadastrar?</span>
      <button @click="fillTestAccount" class="btn-demo">Acesso Rápido</button>
    </div>
  </div>
</div>

  <div v-if="showRegister" class="modal-overlay">
    <div class="modal">
      <h3>Register</h3>
      <input v-model="regForm.email" placeholder="Email" class="input" />
      <input v-model="regForm.password" type="password" placeholder="Password" class="input" />
      <div class="modal-actions">
        <button @click="doRegister">Register</button>
        <button @click="showRegister = false" class="secondary">Close</button>
      </div>
      <div v-if="authError" class="error">{{ authError }}</div>
    </div>
  </div>
</template>

<style scoped>
.loading-overlay {
  position: fixed; top: 0; left: 0; width: 100%; height: 100%;
  background: #0a0a0a; color: white;
  display: flex; align-items: center; justify-content: center;
  z-index: 9999;
}
.loader-content { text-align: center; }
.spinner {
  border: 4px solid rgba(255, 255, 255, 0.1);
  border-left-color: #8b31ff;
  border-radius: 50%; width: 40px; height: 40px;
  animation: spin 1s linear infinite;
  margin: 0 auto 20px;
}
@keyframes spin { to { transform: rotate(360deg); } }

.modal-overlay {
  position: fixed;
  top: 0; left: 0; width: 100%; height: 100%;
  background: rgba(0, 0, 0, 0.8);
  display: flex; justify-content: center; align-items: center;
  z-index: 200;
}
.modal {
  background: #222; padding: 20px; border-radius: 8px; width: 300px;
  border: 1px solid #8b31ff; color: white;
}
.input {
  width: 100%; margin-bottom: 10px; padding: 8px;
  background: #333; border: 1px solid #444; color: white; border-radius: 4px;
}
.modal-actions { display: flex; gap: 10px; }
.error { color: #ff4444; margin-top: 10px; font-size: 0.9em; }
.secondary { background: #444; }
button { cursor: pointer; }

.demo-section {
  margin-top: 15px;
  padding-top: 15px;
  border-top: 1px solid #333;
  display: flex;
  flex-direction: column;
  gap: 8px;
  text-align: center;
}

.demo-section span {
  font-size: 0.8rem;
  color: #888;
}

.btn-demo {
  background: transparent !important;
  border: 1px solid #8b31ff !important;
  color: #8b31ff !important;
  padding: 8px !important;
  font-size: 0.9rem !important;
  width: 100%;
}

.btn-demo:hover {
  background: #8b31ff !important;
  color: white !important;
}
</style>