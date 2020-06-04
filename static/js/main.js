import Vue from 'vue'
import axios from 'axios'
import VueAxios from 'vue-axios'
import VueMoment from 'vue-moment'

import MeetingRoom from "../../front/components/meeting-room.vue";

import awaseInput from "../../front/components/awase/input.vue";
import awaseCreateForm from "../../front/components/awase/create-calendar-form.vue";
import awaseUpdateForm from "../../front/components/awase/update-calendar-form.vue";

import MemberEmailConfirm from "../../front/components/email_confirm.vue";

Vue.use(VueAxios, axios)
Vue.use(VueMoment);

var app = new Vue({
  el: "#vue-app",
  components: {
    // home/index 用の例会教室表示コンポーネント
    'meeting-room': MeetingRoom,

    // awase/calendar/<int:pk>/input/ のコンポーネント
    'awase-input': awaseInput,
    'create-calendar-form': awaseCreateForm,
    'update-calendar-form': awaseUpdateForm,

    'member-email-confirm': MemberEmailConfirm,
  }
})

app.axios.defaults.xsrfCookieName = "csrftoken";
app.axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";