<template>
  <div class="message-wraper">
    <div v-for="key in displaying" :key="key" class="popup-message">
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
    const before_display = computed(() => {
      const keys = Object.keys(messages.value);
      return keys.filter(key => !messages.value[key].completed && !messages.value[key].displayed)
    })
    const displaying = computed(() => {
      const keys = Object.keys(messages.value);
      return keys.filter(key => !messages.value[key].completed && messages.value[key].displayed)
    })

    watchEffect(() => {
      for (const key of before_display.value) {
        store.commit('message/displayed', key)
        setTimeout(() => {
          store.commit('message/completed', key)
        }, MESSAGE_DURATION);
      }
    })

    return {
      messages,
      before_display,
      displaying
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
