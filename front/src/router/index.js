import { createRouter, createWebHistory } from 'vue-router'
import store from '../store'

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
    component: () => import(/* webpackChunkName: "read" */ '../pages/mail/content.vue'),
    props: route => ({
      id: Number(route.params.id)
    })
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
  },
  {
    path: '/sound',
    name: 'sound:index',
    component: () => import(/* webpackChunkName: "sound" */ '../pages/sound/index.vue')
  },
  {
    path: '/sound/:id(\\d+)',
    name: 'sound:content',
    component: () => import(/* webpackChunkName: "sound" */ '../pages/sound/content.vue'),
    props: route => ({
      id: Number(route.params.id)
    })
  },
  {
    path: '/kansou',
    name: 'kansou:index',
    component: () => import(/* webpackChunkName: "kansou" */ '../pages/kansou/index.vue')
  },
]

const router = createRouter({
  history: createWebHistory("/"),
  routes,
  base: "/"
})

router.beforeEach((to, from, next) => {
  store.commit("updateLastPath", from);
  next();
})

export default router
