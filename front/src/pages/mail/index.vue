<template>
  <div>
    <h1>mail/read - index</h1>
  </div>
</template>

<script>
import { computed } from 'vue'
import { useStore } from "vuex"
// import { useRouter } from 'vue-router'
export default {
  setup() {
    const store = useStore();
    // const router = useRouter();

    const messages = computed(() => store.state.read.messages);

    // console.log(router)
    store.dispatch('read/firstLoadMessage')
    return{
      messages
    }
  }
}
</script>