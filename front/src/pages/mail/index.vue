<template>
  <div>
    <h1>mail/read - index</h1>
    <one-message-row v-for="mes in messages" :key="mes.id" :message="mes" />
  </div>
</template>

<script>
import { computed } from 'vue'
import { useStore } from "vuex"
import oneMessageRow from './components/one-message-row.vue'
export default {
  components: {
    oneMessageRow
  },
  setup() {
    const store = useStore();
    const messages = computed(() => store.state.read.messages);
    store.dispatch('read/firstLoadMessage');
    return{
      messages
    }
  }
}
</script>