import Vue from 'vue'
import axios from 'axios'
import router from '../../front/router'
import store from '../../front/store'
import VueAxios from 'vue-axios'
import VueMoment from 'vue-moment'
import VueMeta from 'vue-meta'

// v-calendar
import Calendar from 'v-calendar/lib/components/calendar.umd'
import DatePicker from 'v-calendar/lib/components/date-picker.umd'

// infinite loading
import InfiniteLoading from 'vue-infinite-loading';

// vue-select
import vSelect from 'vue-select'
import 'vue-select/dist/vue-select.css';

// 共通コンポーネント
import App from '../../front/components/App.vue';

import back from '../../front/components/back-arrow.vue';

import MeetingRoom from "../../front/components/meeting-room.vue";

import soundUpload from "../../front/components/sound/upload.vue";
import soundPlaylist from "../../front/components/sound/playlist.vue";

import awaseCalendar from "../../front/components/awase/calendar.vue";
import awaseCalendarMenu from "../../front/components/awase/calendar-menu.vue";
import awaseCalendarExample from "../../front/components/awase/calendar-example.vue";
import awaseInput from "../../front/components/awase/input.vue";
import awaseCreateForm from "../../front/components/awase/create-calendar-form.vue";
import awaseUpdateForm from "../../front/components/awase/update-calendar-form.vue";
import awaseUpdateHours from "../../front/components/awase/update-hours.vue";

import MemberEmailConfirm from "../../front/components/email_confirm.vue";

Vue.use(VueAxios, axios)
Vue.use(VueMoment)
Vue.use(VueMeta)

Vue.use(InfiniteLoading, {
  
});

Vue.component('v-calendar', Calendar)
Vue.component('v-date-picker', DatePicker)

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

    // sound のコンポーネント
    'sound-upload': soundUpload,
    'sound-playlist': soundPlaylist,

    // awase/calendar/ のコンポーネント
    'awase-calendar': awaseCalendar,
    'awase-calendar-menu': awaseCalendarMenu,
    'awase-calendar-example': awaseCalendarExample,

    // awase/calendar/<int:pk>/input/ のコンポーネント
    'awase-input': awaseInput,
    'awase-create-calendar-form': awaseCreateForm,
    'awase-update-calendar-form': awaseUpdateForm,
    'awase-update-hours': awaseUpdateHours,

    'member-email-confirm': MemberEmailConfirm,
  }
})

app.axios.defaults.xsrfCookieName = "csrftoken";
app.axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";