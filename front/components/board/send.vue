<template>
  <send-input
    v-if="process==0"
    @confirm="goToConfirm" />
  <send-confirm
    v-else-if="process==1"
    @send="send"
    @backToInput="backToInput" />
  <send-finish v-else-if="process==2" />
  <div v-else>error</div>
</template>

<script>
import sendInput from './send-input.vue';
import sendConfirm from './send-confirm.vue';
import sendFinish from './send-finish-and-complete.vue';
export default {
  name: 'send',
  components: {
    sendInput,
    sendConfirm,
    sendFinish
  },
  data: () => {
    return {
      process: 0,
    }
  },
  methods: {
    goToConfirm (){
      this.process = 1;
    },
    backToInput () {
      this.process = 0;
    },
    send () {
      this.process = 2;
      // axios
    }
  }
}
</script>