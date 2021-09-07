<template>
  <div class="message-wraper">
    <div v-for="key in displaying" :key="key" class="popup-message" :class="[select(key).level]">
      <button @click="close(key)" class="popup-close"></button>
      {{select(key).message}}
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

    const select = key => messages.value[key];

    const close = key => store.commit('message/completed', key)

    return {
      messages,
      before_display,
      displaying,
      select,
      close
    }
  }
}
</script>

<style scoped>
.message-wraper{
  position: fixed;
  display: flex;
  box-sizing: border-box;
  flex-direction: column-reverse;
  flex-wrap: wrap;
  justify-content: flex-end;
  text-align: left;
  bottom: 0;
  right: 0;
  width: 300px;
  margin: 0 1rem 1rem 0;
}
.popup-message{
  position: relative;
  display: inline-block;
  box-sizing: border-box;
  width: 300px;
  padding: 1rem 0.75rem;
  margin: 0.25rem 0;
  border: 2px solid transparent;
  border-radius: 0.5rem;
  font-size: 12px;
}
.popup-message.success{
  border-color: #28a745;
  background-color: #f3fcf5;
}
.popup-message.error{
  border-color: #dc3545;
  background-color: #fdf1f2;
}
.popup-message.warning{
  border-color: #ffc107;
  background-color: #fffcf5;
}
.popup-message.info{
  border-color: #17a2b8;
  background-color: #f2fcfd;
}
.popup-close{
  background: transparent;
  border: none;
  padding: 0 1rem;
  position: relative;
}
.popup-close::after,
.popup-close::before{
  content: "";
  display: block;
  height: 12px;
  width: 12px;
  position: absolute;
  top: -6px;
  border-top: 1px solid transparent;
  background: rgba(0, 0, 0, 0);
}
.popup-close::after{
  left: 3px;
  transform: rotate(45deg);
}
.popup-close::before{
  left: 11px;
  transform: rotate(-45deg);
}
.popup-message.success .popup-close::after,
.popup-message.success .popup-close::before{
  border-color: #28a745;
}
.popup-message.error .popup-close::after,
.popup-message.error .popup-close::before{
  border-color: #dc3545;
}
.popup-message.warning .popup-close::after,
.popup-message.warning .popup-close::before{
  border-color: #ffc107;
}
.popup-message.info .popup-close::after,
.popup-message.info .popup-close::before{
  border-color: #17a2b8;
}
</style>
