<template>
  <div class="message-wraper">
    <div v-for="key in display_keys" :key="key" class="popup-message">
      {{messages[key].message}}
    </div>
  </div>
</template>

<script>
import { computed, watchEffect } from "vue";
import { useStore } from "vuex";

const MESSAGE_DURATION = 5000;
export default {
  name: "message",
  setup() {
    // vuexから表示するmessageを取得
    const store = useStore();
    const messages = computed(() => store.state.message.messages);
    const display_keys = computed(() => {
      const keys = Object.keys(messages.value);
      return keys.filter(key => !messages.value[key].completed)
    })

    watchEffect(() => {
      // console.log(display_keys.value)
      for (let i = 0; i < display_keys.value.length; i++) {
        store.commit('message/displayed', display_keys.value[i])
        setTimeout(() => {
          store.commit('message/completed', display_keys.value[i])}, MESSAGE_DURATION);
        }
    })


    return {
      messages,
      display_keys
    }
  }
}
</script>

<style scoped>
.message-wraper{
  position: fixed;
  display: flex;
  flex-direction: column-reverse;
  flex-wrap: wrap;
  justify-content: flex-end;
  bottom: 1rem;
  right: 1rem;
  width: 300px;
}
.popup-message{
  position: relative;
  display: inline-block;
  width: 300px;
}
</style>
