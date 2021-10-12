import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import(/* webpackChunkName: "home" */ '../pages/index/index.vue')
  },
  {
    path: '/mail/send',
    name: 'mail:send',
    component: () => import(/* webpackChunkName: "send" */ '../pages/mail/send.vue')
  },
  {
    path: '/about',
    name: 'About',
    component: () => import(/* webpackChunkName: "about" */ '../views/About.vue')
  }
]

const router = createRouter({
  history: createWebHistory("/"),
  routes,
  base: "/"
})

export default router
