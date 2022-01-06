import { createRouter, createWebHistory } from "vue-router";
import store from "../store";

const routes = [
  {
    path: "/",
    name: "Home",
    component: () => import(/* webpackChunkName: "home" */ "../pages/index/index.vue")
  },
  {
    path: "/mail/",
    name: "mail:index",
    component: () => import(/* webpackChunkName: "read" */ "../pages/mail/index.vue")
  },
  {
    path: "/mail/:id(\\d+)/",
    name: "mail:content",
    component: () => import(/* webpackChunkName: "read" */ "../pages/mail/content.vue"),
    props: route => ({
      id: Number(route.params.id)
    })
  },
  {
    path: "/mail/send/",
    name: "mail:send",
    component: () => import(/* webpackChunkName: "send" */ "../pages/mail/send.vue")
  },
  {
    path: "/mail/send/confirm/",
    name: "mail:send-confirm",
    component: () => import(/* webpackChunkName: "send" */ "../pages/mail/send-confirm.vue")
  },
  {
    path: "/photo/",
    name: "photo:index",
    component: () => import(/* webpackChunkName: "photo" */ "../pages/photo/index.vue")
  },
  {
    path: "/sound/",
    name: "sound:index",
    component: () => import(/* webpackChunkName: "sound" */ "../pages/sound/index.vue")
  },
  {
    path: "/sound/:id(\\d+)/",
    name: "sound:content",
    component: () => import(/* webpackChunkName: "sound" */ "../pages/sound/content.vue"),
    props: route => ({
      id: Number(route.params.id)
    })
  },
  {
    path: "/kansou/",
    name: "kansou:index",
    component: () => import(/* webpackChunkName: "kansou" */ "../pages/kansou/index.vue")
  },
  {
    path: "/mypage/",
    name: "mypage:index",
    component: () => import(/* webpackChunkName: "mypage" */ "../pages/mypage/index.vue")
  },
  {
    path: "/mypage/profile/",
    name: "mypage:profile",
    component: () => import(/* webpackChunkName: "mypage" */ "../pages/mypage/profile.vue")
  },
  {
    path: "/mypage/mail-settings/",
    name: "mypage:mail-settings",
    component: () => import(/* webpackChunkName: "mypage" */ "../pages/mypage/mail-settings.vue")
  },
  {
    path: "/mypage/mail-test/",
    name: "mypage:mail-test",
    component: () => import(/* webpackChunkName: "mypage" */ "../pages/mypage/mail-test.vue")
  },
  {
    path: "/mypage/oauth/",
    name: "mypage:oauth",
    component: () => import(/* webpackChunkName: "mypage" */ "../pages/mypage/oauth.vue")
  },
  {
    path: "/mypage/invite/",
    name: "mypage:invite",
    component: () => import(/* webpackChunkName: "mypage-invite" */ "../pages/mypage/invite.vue")
  },
  {
    path: "/movie/",
    name: "movie:index",
    component: () => import(/* webpackChunkName: "movie" */ "../pages/movie/index.vue")
  },
];

const router = createRouter({
  history: createWebHistory("/"),
  routes,
  base: "/"
});

router.beforeEach((to, from, next) => {
  if (to.path.slice(-1) !== "/") {
    return next({
      ...to,
      path: `${to.path}/`,
    });
  }
  store.commit("setMenuStatus", "menuClosed");
  store.commit("updateLastPath", from);
  next();
});

export default router;
