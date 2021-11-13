import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import(/* webpackChunkName: "home" */ '../pages/index/index.vue')
  },
  {
    path: '/mail',
    name: 'mail:index',
    component: () => import(/* webpackChunkName: "read" */ '../pages/mail/index.vue')
  },
  {
    path: '/mail/:id(\\d+)',
    name: 'mail:content',
    component: () => import(/* webpackChunkName: "read" */ '../pages/mail/content.vue')
  },
  {
    path: '/mail/send',
    name: 'mail:send',
    component: () => import(/* webpackChunkName: "send" */ '../pages/mail/send.vue')
  },
  {
    path: '/mail/send/confirm',
    name: 'mail:send-confirm',
    component: () => import(/* webpackChunkName: "send" */ '../pages/mail/send-confirm.vue')
  },
  {
    path: '/photo',
    name: 'photo:index',
    component: () => import(/* webpackChunkName: "photo" */ '../pages/photo/index.vue')
  }
]

const router = createRouter({
  history: createWebHistory("/"),
  routes,
  base: "/"
})

export default router
