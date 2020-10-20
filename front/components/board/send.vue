<template>
  <send-input v-if="process==0" />
  <send-confirm v-else-if="process==1" />
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
  }
}
</script>