import { createApp } from "vue";
import App from "./PrivateApp.vue";
import store from "./store";
import router from "./router";

createApp(App).use(router).use(store).mount("#app");
