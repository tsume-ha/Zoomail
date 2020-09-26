<template>
  <div>
    <h3>メーリス一覧</h3>
    <one-content
      v-for="message in messages"
      :key="message.id"
      :message="message" />
    <infinite-loading
      @infinite="infiniteLoad"
    ></infinite-loading>
  </div>
</template>

<script>
import oneContent from './index-one-content.vue';
export default {
  name: 'index',
  components: {
    oneContent
  },
  computed: {
    messages () {
      return this.$store.state.read.messages;
    }
  },
  created () {
    if (this.messages.length) {
      return;
    }
    // this.$store.dispatch('read/loadMessages');
  },
  methods: {
    infiniteLoad ($state) {
      this.$store.dispatch('read/loadMessages')
      .then((res) => {
        console.log('complete')
        console.log(res)

      })
      // $state.loaded();
    }
  }
}
</script>