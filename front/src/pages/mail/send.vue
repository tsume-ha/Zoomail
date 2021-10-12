<template>
  <div>
    <h1>mail/send</h1>
    <p>
    title
    <input type="text" title="title" v-model="title" />
    </p>
  </div>
</template>

<script>
import { computed } from 'vue'
import { useStore } from "vuex";
export default {
  setup() {
    const store = useStore();
    const title = computed({
      get: () => store.state.send.title["value"],
      set: value => store.commit('send/setTitle', value)
    })
    return{
      title
    }
  }
}
</script>