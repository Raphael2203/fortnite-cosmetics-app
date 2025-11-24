import axios from "axios"

const BASE = import.meta.env.VITE_API_URL

const API = axios.create({
  baseURL: BASE,
  timeout: 5000
})

const setToken = (token: string | null) => {
  if (token) {
    API.defaults.headers.common["Authorization"] = `Bearer ${token}`
    try { localStorage.setItem("fc_token", token) } catch {}
  } else {
    delete API.defaults.headers.common["Authorization"]
    try { localStorage.removeItem("fc_token") } catch {}
  }
}

try {
  const saved = localStorage.getItem("fc_token")
  if (saved) setToken(saved)
} catch {}

export default {
  register: (payload: { email: string; password: string }) =>
    API.post("/auth/register/", payload),

  login: (payload: { email: string; password: string }) =>
    API.post("/auth/login/", payload),

  me: () => API.get("/auth/me/"),

  setToken,
  clearToken: () => setToken(null),

  listCosmetics: (params?: any) => API.get("/cosmetics/", { params }),
  getCosmetic: (id: number) => API.get(`/cosmetics/${id}/`),

  buyCosmetic: (id: number) => API.post(`/purchases/buy/cosmetic/${id}/`),
  buyBundle: (id: number) => API.post(`/purchases/buy/bundle/${id}/`),
  returnCosmetic: (id: number) => API.post(`/purchases/return/cosmetic/${id}/`),
  history: () => API.get("/purchases/history/"),

  listUsers: (params?: any) => API.get("/users/", { params }),
  getUser: (id: number) => API.get(`/users/${id}/`)
}
