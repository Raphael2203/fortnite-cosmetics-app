import axios from 'axios'

const RAW_BASE = (import.meta.env?.VITE_API_URL as string) || ''

let BASE = RAW_BASE || ''

if (typeof window !== 'undefined') {
  try {
    if (!BASE) {
      BASE = `${window.location.protocol}//${window.location.hostname}:8000`
    } else {
      try {
        const u = new URL(BASE)
        if (u.hostname === 'backend') {
          u.hostname = window.location.hostname
          BASE = u.toString()
        }
      } catch {
      }
    }
  } catch {
  }
}

if (!BASE) BASE = 'http://localhost:8000'

const API = axios.create({
  baseURL: BASE,
  timeout: 5000
})

const setToken = (token: string | null) => {
  if (token) {
    API.defaults.headers.common['Authorization'] = `Bearer ${token}`
    try { localStorage.setItem('fc_token', token) } catch {}
  } else {
    delete API.defaults.headers.common['Authorization']
    try { localStorage.removeItem('fc_token') } catch {}
  }
}

try {
  const saved = localStorage.getItem('fc_token')
  if (saved) setToken(saved)
} catch {}

export default {
  // auth
  register: (payload: { email: string; password: string }) => API.post('/auth/register', payload),
  login: (payload: { email: string; password: string }) => API.post('/auth/login', payload),
  me: () => API.get('/auth/me'),
  setToken,
  clearToken: () => setToken(null),

  // cosmetics
  listCosmetics: (params?: any) => API.get('/cosmetics', { params }),
  getCosmetic: (id: number) => API.get(`/cosmetics/${id}`),
  // purchases
  buyCosmetic: (id: number) => API.post(`/purchases/buy/cosmetic/${id}`),
  buyBundle: (id: number) => API.post(`/purchases/buy/bundle/${id}`),
  returnCosmetic: (id: number) => API.post(`/purchases/return/cosmetic/${id}`),
  history: () => API.get('/purchases/history'),
  // users
  listUsers: (params?: any) => API.get('/users', { params }),
  getUser: (id: number) => API.get(`/users/${id}`)
}
