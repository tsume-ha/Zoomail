import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter)

const routes = [
  {
    path: '/read/_/',
    name: 'index',
    component: () => import(/* webpackChunkName: "read" */ '../components/board/index.vue'),
    meta: 'read:index',
  },
  {
    path: '/read/_/content/:id/',
    name: 'content',
    component: () => import(/* webpackChunkName: "read" */ '../components/board/content.vue'),
    props: routes => ({
      id: Number(routes.params.id)
    }),
    meta: 'read:content'
  },
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
