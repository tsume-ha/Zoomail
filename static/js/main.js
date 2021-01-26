import Vue from 'vue'
import axios from 'axios'
import router from '../../front/router'
import store from '../../front/store'
import VueAxios from 'vue-axios'
import VueMoment from 'vue-moment'
import VueMeta from 'vue-meta'

// infinite loading
import InfiniteLoading from 'vue-infinite-loading';

// vue-select
import vSelect from 'vue-select'
import 'vue-select/dist/vue-select.css';

// 共通コンポーネント
import App from '../../front/components/App.vue';

import back from '../../front/components/back-arrow.vue';

import MeetingRoom from "../../front/components/meeting-room.vue";

import awaseUpdateForm from "../../front/components/awase/update-calendar-form.vue";

import MemberEmailConfirm from "../../front/components/email_confirm.vue";

Vue.use(VueAxios, axios)
Vue.use(VueMoment)
Vue.use(VueMeta)

Vue.use(InfiniteLoading, {
  
});

Vue.component('v-select', vSelect)

var app = new Vue({
  router,
  store,
  el: "#vue-app",
  components: {
    // 共通コンポーネント、Wrapper
    'App': App,

    // 「戻る」リンク用のコンポーネント
    'back': back,

    // home/index 用の例会教室表示コンポーネント
    'meeting-room': MeetingRoom,

    // awase のコンポーネント
    'awase-update-calendar-form': awaseUpdateForm,

    'member-email-confirm': MemberEmailConfirm,
  }
})

app.axios.defaults.xsrfCookieName = "csrftoken";
app.axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";