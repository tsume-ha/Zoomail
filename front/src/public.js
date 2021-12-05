import { createApp } from "vue";
import { createRouter, createWebHistory } from "vue-router";
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




createApp(App).use(router).mount("#app");
