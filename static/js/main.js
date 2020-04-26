window.Vue = require("vue");
import Example from "../../front/components/test.vue";

var app = new Vue({
  el: "#main",
  components: {
    "example-component": Example,
  }
});
