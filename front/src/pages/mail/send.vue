<template>
  <div>
    <h1>mail/send</h1>
    <send-input-title />
    <send-input-content />
    <send-input-from />

  </div>
</template>

<script>
// import { computed, onMounted } from 'vue'
// import { useStore } from "vuex";
import sendInputTitle from "./components/send-input-title.vue"
import sendInputContent from "./components/send-input-content.vue"
// import sendInputTo from "./components/send-input-to.vue"
// vue-selectがvue3にまだ対応していないので保留
import sendInputFrom from "./components/send-input-from.vue"
export default {
  components: {
    sendInputTitle, sendInputContent, sendInputFrom
  },
  setup() {
    // const store = useStore();

    return{
      // title,
      // tos,
      // writer_id
    }
  }
}
</script>