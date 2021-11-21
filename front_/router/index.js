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
    path: '/sound/upload/',
    name: 'sound:upload',
    component: () => import(/* webpackChunkName: "sound" */'../components/sound/upload.vue'),
    meta: 'sound:upload',
  },
  {
    path: '/sound/:id/',
    name: 'sound:playlist',
    component: () => import(/* webpackChunkName: "sound" */'../components/sound/playlist.vue'),
    meta: 'sound:playlist',
  },
  {
    path: '/mypage/',
    name: 'mypage:index',
    component: () => import(/* webpackChunkName: "mypage" */'../components/mypage/index.vue'),
    meta: 'mypage:index',
  },
  {
    path: '/mypage/oauth/',
    name: 'mypage:oauth',
    component: () => import(/* webpackChunkName: "mypage" */'../components/mypage/oauth.vue'),
    meta: 'mypage:oauth',
  },
  {
    path: '/mypage/info-update/',
    name: 'mypage:info-update',
    component: () => import(/* webpackChunkName: "mypage" */'../components/mypage/info-update.vue'),
    meta: 'mypage:info-update',
  },
  {
    path: '/mypage/mail-settings/',
    name: 'mypage:mail-settings',
    component: () => import(/* webpackChunkName: "mypage" */'../components/mypage/mail-settings.vue'),
    meta: 'mypage:mail-settings',
  },
  {
    path: '/mypage/mail-test/',
    name: 'mypage:mail-test',
    component: () => import(/* webpackChunkName: "mypage" */'../components/mypage/mail-test.vue'),
    meta: 'mypage:mail-test',
  },
  {
    path: '/mypage/register/',
    name: 'mypage:register',
    component: () => import(/* webpackChunkName: "mypage-register" */'../components/mypage/register.vue'),
    meta: 'mypage:register',
  },
  {
    path: '/meeting_room/',
    name: 'meeting_room',
    component: () => import(/* webpackChunkName: "meeting_room" */'../components/meeting_room/index.vue'),
    meta: 'meeting_room',
  },
  {
    path: '/meeting_room/register/',
    name: 'meeting_room:register',
    component: () => import(/* webpackChunkName: "meeting_room-register" */'../components/meeting_room/register-column.vue'),
    meta: 'meeting_room:register',
  },
  {
    path: '/*',
    name: '404',
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