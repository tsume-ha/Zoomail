<template>
  <div>
    <h1>mail/send</h1>
    <send-input-title />
    <send-input-content />

  </div>
</template>

<script>
import { computed, onMounted } from 'vue'
import { useStore } from "vuex";
import sendInputTitle from "./components/send-input-title.vue"
import sendInputContent from "./components/send-input-content.vue"
export default {
  components: {
    sendInputTitle, sendInputContent
  },
  setup() {
    const store = useStore();

    // Field value
    const title = computed({
      get: () => store.state.send.title["value"],
      set: value => store.commit('send/setTitle', value)
    });

    const tos = computed({
      get: () => store.state.send.tos["value"],
      set: value => store.commit('send/setTos', value)
    });
    const writer_id = computed({
      get: () => store.state.send.writer_id["value"],
      set: value => store.commit('send/setWriter_id', value)
    });

    // On mounted
    onMounted(() => {
      if (!writer_id.value && !!store.state.user.id) {
        store.commit('send/setWriter_id', store.state.user.id)
      }
    });
    return{
      title,
      tos,
      writer_id
    }
  }
}
</script>