import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter)

const routes = [
  {
    path: '/read/_/',
    name: 'index',
    component: () => import(/* webpackChunkName: "read" */ '../components/board/index.vue')
  },
  {
    path: '/read/_/content/:id/',
    name: 'content',
    component: () => import(/* webpackChunkName: "read" */ '../components/board/content.vue'),
    props: routes => ({
      id: Number(routes.params.id)
    })
  },
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
