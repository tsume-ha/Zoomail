import { createApp } from "vue";
import App from "./FirstRegisterApp.vue";

import { library } from "@fortawesome/fontawesome-svg-core";
import { fas } from "@fortawesome/free-solid-svg-icons";
import { fab } from "@fortawesome/free-brands-svg-icons";
import { far } from "@fortawesome/free-regular-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
library.add(fas, fab, far);

import "@/assets/sass/main.scss";

createApp(App).component("Icon", FontAwesomeIcon).mount("#app");
