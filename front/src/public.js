import { createApp } from "vue";
import { createRouter, createWebHistory } from "vue-router";
import BootstrapVue3 from "bootstrap-vue-3";
import App from "./PublicApp.vue";

import "bootstrap/dist/css/bootstrap.css";
import "bootstrap-vue-3/dist/bootstrap-vue-3.css";

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


createApp(App).use(router).use(BootstrapVue3).mount("#app");
