import { createApp } from "vue";
import { createRouter, createWebHistory } from "vue-router";
import { createStore } from "vuex";
import message from "./store/message";
import App from "./PublicApp.vue";

import "./registerServiceWorker.js";

import { library } from "@fortawesome/fontawesome-svg-core";
import { fas } from "@fortawesome/free-solid-svg-icons";
import { fab } from "@fortawesome/free-brands-svg-icons";
import { far } from "@fortawesome/free-regular-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
library.add(fas, fab, far);

import "@/assets/sass/main.scss";

// router settings
import Index from "@/pages/public/Index.vue";
import Login from "@/pages/public/Login.vue";
import LoggedOut from "@/pages/public/LoggedOut.vue";
const routes = [
  {
    path: "/",
    name: "index",
    component: Index
  },
  {
    path: "/login/",
    name: "login",
    component: Login
  },
  {
    path: "/logged_out/",
    name: "logged_out",
    component: LoggedOut
  },
];
const router = createRouter({
  history: createWebHistory("/"),
  routes,
  base: "/"
});
router.beforeEach((to, from, next) => {
  if (to.path.slice(-1) !== "/") {
    return next(`${to.path}/`);
  }
  if (to.name === "login" || to.name === "logged_out") {
    store.commit("setIsMenuOpen", true);
  } else {
    store.commit("setIsMenuOpen", false);
  }
  next();
});


const store = createStore({
  strict: process.env.NODE_ENV !== "production",
  state: {
    isMenuOpen: false,
  },
  mutations: {
    setIsMenuOpen(state, bool) {
      state.isMenuOpen = bool;
    }
  },
  modules: { message }
});



createApp(App).use(router).use(store).component("Icon", FontAwesomeIcon).mount("#app");
