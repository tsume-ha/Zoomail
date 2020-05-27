import Vue from 'vue'
import axios from 'axios'
import VueAxios from 'vue-axios'
import VueMoment from 'vue-moment'
import MeetingRoom from "../../front/components/meeting-room.vue";

import awaseInput from "../../front/components/awase/input.vue";

Vue.use(VueAxios, axios)
Vue.use(VueMoment);
new Vue({
  el: "#meeting-room",
  components: {
    'meeting-room': MeetingRoom
  }
})
new Vue({
  el: "#vue-app",
  components: {
    'awase-input': awaseInput
  }
})