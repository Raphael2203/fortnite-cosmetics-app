<script setup lang="ts">
import { ref, onMounted, watch, computed } from 'vue'
import api from './services/api'

// Estados
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
const activeTab = ref<'comprados' | 'vendidos'>('comprados')

// Funções de Banco e Auth
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

// Histórico
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

const sellItem = async (cosmeticId: number) => {
  if (!confirm("Deseja devolver este item? Os V-Bucks serão estornados.")) return
  try {
    await api.returnCosmetic(cosmeticId)
    await loadMe()
    await loadHistory()
    alert("Item devolvido com sucesso!")
  } catch (err: any) {
    alert("Erro ao devolver item: " + (err.response?.data?.detail ?? err.message))
  }
}

const filteredHistory = computed(() => {
  const returnedIds = history.value.filter(h => h.type === 'return').map(h => h.cosmetic?.id);
  if (activeTab.value === 'comprados') {
    return history.value.filter(h => h.type === 'buy' && h.cosmetic && !returnedIds.includes(h.cosmetic.id));
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
  <nav class="navbar">
    <div class="nav-group links">
      <router-link to="/" class="nav-link">Cosmetics</router-link>
      <router-link to="/users" class="nav-link">Users</router-link>
    </div>

    <div class="nav-group social">
      <a href="https://github.com/Raphael2203/fortnite-cosmetics-app" target="_blank" class="social-link">
        <img src="/github-logo.png" width="20" alt="GitHub">
        <span>GitHub</span>
      </a>
      <a href="https://www.linkedin.com/in/raphael-brito-sa/" target="_blank" class="social-link">
        <img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" width="20" alt="LinkedIn">
        <span>LinkedIn</span>
      </a>
    </div>

    <div class="nav-group auth">
      <template v-if="currentUser">
        <div class="vbucks-badge">
          <img src="https://fortnite-api.com/images/vbuck.png" width="16" />
          <span>{{ currentUser.vbucks }}</span>
        </div>
        <button class="btn-sm" @click="showHistory = !showHistory">History</button>
        <button class="btn-sm logout-btn" @click="logout">Logout</button>
      </template>
      <template v-else>
        <button class="btn-auth" @click="showLogin = true">Login</button>
        <button class="btn-auth register" @click="showRegister = true">Register</button>
      </template>
    </div>
  </nav>

  <main style="padding:16px;">
    <router-view />
  </main>

  <div v-if="showHistory" class="history-panel">
    <h3 class="history-title">History</h3>
    <div class="tab-buttons">
      <button @click="activeTab = 'comprados'" :class="{ active: activeTab === 'comprados' }">COMPRADOS</button>
      <button @click="activeTab = 'vendidos'" :class="{ active: activeTab === 'vendidos' }">VENDIDOS</button>
    </div>

    <div v-if="historyLoading">Loading...</div>
    <ul v-else class="history-list">
      <li v-for="h in filteredHistory" :key="h.id" class="history-item" :class="activeTab">
        <img v-if="h.cosmetic?.image_url" :src="h.cosmetic.image_url" class="item-img" />
        <div class="item-info">
          <div class="item-name">{{ h.cosmetic?.name }}</div>
          <div class="item-footer">
            <small>{{ new Date(h.created_at).toLocaleDateString('pt-BR') }}</small>
            <button v-if="activeTab === 'comprados'" @click="sellItem(h.cosmetic.id)" class="btn-sell">VENDER</button>
          </div>
        </div>
      </li>
    </ul>
    <button @click="showHistory = false" class="btn-close">Close</button>
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
/* NAVBAR */
.navbar {
  padding: 10px 16px;
  border-bottom: 1px solid #333;
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: #1a1a1a;
  color: white;
  flex-wrap: wrap;
  gap: 15px;
}
.nav-group { display: flex; align-items: center; gap: 12px; }
.nav-link { text-decoration: none; color: #42b983; font-weight: bold; font-size: 0.9rem; }
.social-link { display: flex; align-items: center; gap: 5px; color: #eee; text-decoration: none; font-size: 0.8rem; }
.vbucks-badge { display: flex; align-items: center; gap: 5px; background: #2a2a2a; padding: 4px 10px; border-radius: 20px; font-weight: bold; color: #ffd700; font-size: 0.85rem; }
.btn-sm, .btn-auth { padding: 6px 10px; font-size: 0.75rem; font-weight: bold; cursor: pointer; border-radius: 4px; border: none; background: #8b31ff; color: white; }
.logout-btn { background: #444; margin-left: 5px; }

/* MODAIS */
.modal-overlay { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0, 0, 0, 0.8); display: flex; justify-content: center; align-items: center; z-index: 200; }
.modal { background: #222; padding: 20px; border-radius: 8px; width: 300px; border: 1px solid #8b31ff; color: white; }
.input { width: 100%; margin-bottom: 10px; padding: 8px; background: #333; border: 1px solid #444; color: white; border-radius: 4px; }
.error { color: #ff4444; margin-top: 10px; font-size: 0.9em; }

/* HISTÓRICO PANEL */
.history-panel { position: fixed; right: 0; top: 0; height: 100%; width: 380px; background: #111; border-left: 2px solid #8b31ff; padding: 16px; overflow: auto; z-index: 100; }
.tab-buttons { display: flex; gap: 8px; margin-bottom: 20px; }
.tab-buttons button { flex: 1; padding: 8px; background: #333; border: none; color: white; border-radius: 4px; cursor: pointer; }
.tab-buttons button.active { background: #8b31ff; }
.history-item { margin-bottom: 12px; padding: 12px; background: #1e1e2f; border-radius: 6px; display: flex; gap: 12px; }
.history-item.comprados { border-left: 4px solid #007bff; }
.history-item.vendidos { border-left: 4px solid #ff4444; }
.item-img { width: 50px; height: 50px; border-radius: 4px; object-fit: cover; }
.item-info { flex-grow: 1; }
.item-footer { display: flex; justify-content: space-between; align-items: center; margin-top: 4px; }
.btn-sell { background: #ff4444; color: white; border: none; padding: 4px 6px; border-radius: 4px; cursor: pointer; font-size: 0.6rem; font-weight: bold; }

/* RESPONSIVIDADE */
@media (max-width: 768px) {
  .navbar { justify-content: center; }
  .social { display: none; } /* Esconde GitHub/Linkedin no mobile */
  .history-panel { width: 100%; } /* Histórico ocupa tela toda */
}

@media (max-width: 480px) {
  .navbar { gap: 8px; padding: 10px; }
  .nav-link { font-size: 0.8rem; }
  .vbucks-badge { font-size: 0.75rem; padding: 3px 8px; }
}
</style>