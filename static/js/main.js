import Vue from 'vue'
import axios from 'axios'
import VueAxios from 'vue-axios'
import VueMoment from 'vue-moment'
// v-calendar
import Calendar from 'v-calendar/lib/components/calendar.umd'
import DatePicker from 'v-calendar/lib/components/date-picker.umd'


import MeetingRoom from "../../front/components/meeting-room.vue";

import playerUpload from "../../front/components/player/upload.vue";
import playerPlaylist from "../../front/components/player/playlist.vue";

import awaseInput from "../../front/components/awase/input.vue";
import awaseCreateForm from "../../front/components/awase/create-calendar-form.vue";
import awaseUpdateForm from "../../front/components/awase/update-calendar-form.vue";
import awaseUpdateHours from "../../front/components/awase/update-hours.vue";

import MemberEmailConfirm from "../../front/components/email_confirm.vue";

Vue.use(VueAxios, axios)
Vue.use(VueMoment);

Vue.component('v-calendar', Calendar)
Vue.component('v-date-picker', DatePicker)

var app = new Vue({
  el: "#vue-app",
  components: {
    // home/index 用の例会教室表示コンポーネント
    'meeting-room': MeetingRoom,

    // player のコンポーネント
    'player-upload': playerUpload,
    'player-playlist': playerPlaylist,

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