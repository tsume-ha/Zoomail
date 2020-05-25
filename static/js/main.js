import Vue from 'vue'
import axios from 'axios'
import VueAxios from 'vue-axios'
import VueMoment from 'vue-moment'
import MeetingRoom from "../../front/components/meeting-room.vue";

Vue.use(VueAxios, axios)
Vue.use(VueMoment);
new Vue({
  el: "#main",
  components: {
    'meeting-room': MeetingRoom
  }
});