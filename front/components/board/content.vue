<template>
  <div>test{{id}}</div>
</template>

<script>
export default {
  props: {
    id: {type: Number, required: false, default: null}
  },
  data: () => ({
    messageExists: false,

  }),
  computed: {
    messageSelected () {
      return this.id !== null;
    },
    message () {
      if (this.$store.state.read.messages.length == 0) {
        // 直接アクセスして来た場合
        console.log('直接アクセス')
      }
      return this.$store.state.read.messages.find(obj => obj.id == this.id);
    }
  }

}
</script>

