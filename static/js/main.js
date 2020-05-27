import Vue from 'vue'
import axios from 'axios'
import VueAxios from 'vue-axios'
import VueMoment from 'vue-moment'
import Example from "../../front/components/test.vue";
import MeetingRoom from "../../front/components/meeting-room.vue";

Vue.use(VueAxios, axios)
Vue.use(VueMoment);
new Vue({
  el: "#main",
  components: {
    "example-component": Example,
  }
});
new Vue({
  el: "#meeting-room",
  components: {
    'meeting-room': MeetingRoom
  }
})