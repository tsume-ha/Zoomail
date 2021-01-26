import Vue from 'vue'
import VueRouter from 'vue-router'
import NotFoundComponent from '../components/404.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/read/',
    name: 'index',
    component: () => import(/* webpackChunkName: "read" */'../components/board/index.vue'),
    meta: 'read:index',
  },
  {
    path: '/read/content/:id/',
    name: 'content',
    component: () => import(/* webpackChunkName: "read" */'../components/board/content.vue'),
    props: routes => ({
      id: Number(routes.params.id)
    }),
    meta: 'read:content'
  },
  {
    path: '/send/',
    name: 'send',
    component: () => import(/* webpackChunkName: "send" */'../components/board/send.vue'),
    meta: 'send:index',
  },
  {
    path: '/awase/:id/',
    name: 'awase:calendar',
    component: () => import(/* webpackChunkName: "awase" */'../components/awase/calendar-index.vue'),
    meta: 'awase:calendar',
  },
  {
    path: '/awase/:id/input',
    name: 'awase:calendar',
    component: () => import(/* webpackChunkName: "awase" */'../components/awase/input.vue'),
    meta: 'awase:calendar',
  },
  {
    path: '*',
    component: NotFoundComponent
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes,
  scrollBehavior (to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    } else if (to.meta == 'read:index' && from.meta == 'read:content') {
      return {
        selector: '#message-id-' + String(from.params.id)
      }
    } else {
      return { x: 0, y: 0 }
    }
  }
})

export default router
