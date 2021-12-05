import { createApp } from "vue";
import { createRouter, createWebHistory } from "vue-router";
import { createStore } from "vuex";
import App from "./PublicApp.vue";

import "@/assets/sass/main.scss";

// router settings
import Index from "@/pages/public/Index.vue";
import Login from "@/pages/public/Login.vue";
const routes = [
  {
    path: "/",
    name: "index",
    component: Index
  },
  {
    path: "/login",
    name: "login",
    component: Login
  },
];
const router = createRouter({
  history: createWebHistory("/"),
  routes,
  base: "/"
});
router.beforeEach((to, from, next) => {
  if (to.name === "login") {
    store.commit("set", true);
  } else {
    store.commit("set", false);
  }
  next();
});


const store = createStore({
  strict: process.env.NODE_ENV !== "production",
  state: {
    isMenuOpen: false,
  },
  mutations: {
    set (state, bool) {
      state.isMenuOpen = bool;
    }
  }
});



createApp(App).use(router).use(store).mount("#app");
