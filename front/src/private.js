import { createApp } from "vue";
import App from "./PrivateApp.vue";
import store from "./store";
import router from "./router";

import "@/assets/sass/main.scss";

createApp(App).use(router).use(store).mount("#app");
