import { createApp } from "vue";
import App from "./PrivateApp.vue";
import store from "./store";
import router from "./router";

import { library } from "@fortawesome/fontawesome-svg-core";
import { faUserSecret } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
library.add(faUserSecret);


import "@/assets/sass/main.scss";

createApp(App).use(router).use(store).component("font-awesome-icon", FontAwesomeIcon).mount("#app");
