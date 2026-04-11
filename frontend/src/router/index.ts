import { createRouter, createWebHistory } from 'vue-router'
import CosmeticsList from '../views/CosmeticsList.vue'
import CosmeticDetail from '../views/CosmeticDetail.vue'
import UsersList from '../views/UsersList.vue'
import UserProfile from '../views/UserProfile.vue'

const routes = [
  { path: '/', component: CosmeticsList, props: {defaultFilter : {is_on_sale: true}} },
  { path: '/cosmetics/:id', component: CosmeticDetail, props: true },
  { path: '/users', component: UsersList },
  { path: '/users/:id', component: UserProfile, props: true }
]

// use Vite base url (import.meta.env.BASE_URL) for proper history base
export default createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})
