<template>
  <div>
    <h1>mail/read - index</h1>
    <transition-group name="message-row">
      <one-message-row v-for="mes in messages" :key="mes.id" :message="mes" class="one-message-row" />
    </transition-group>
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

<style scoped>
.one-message-row{
  display: block;
}
.message-row-leave-active{
  position: absolute;
}
.message-row-move{
  transition: all 0.5s;
}
/* .message-row-enter-active{
  transition: all 5s;
}
.message-row-enter{
  opacity: 0;
}
.message-row-enter-to{
  opacity: 1;
} */
</style>