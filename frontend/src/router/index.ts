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

export default createRouter({
  history: createWebHistory((import.meta as any).env.BASE_URL),
  routes
})
