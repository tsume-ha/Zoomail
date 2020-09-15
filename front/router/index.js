import Vue from 'vue'
import VueRouter from 'vue-router'
import readIndex from '../components/board/index.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/read/_/',
    name: 'index',
    component: readIndex
  },
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
