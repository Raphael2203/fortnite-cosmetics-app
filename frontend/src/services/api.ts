import axios from 'axios'

// use Vite env var when available (set via docker-compose or .env), otherwise fallback
const BASE = (import.meta.env?.VITE_API_URL as string) || 'http://localhost:8000'

const API = axios.create({
  baseURL: BASE,
  timeout: 5000
})

export default {
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
