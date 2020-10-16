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
  data: () => ({
  }),
  computed: {
    messages () {
      return this.$store.state.read.messages;
    }
  },
  methods: {
    infiniteLoad ($state) {
      this.$store.dispatch('read/loadMessages').then((h) => {
        console.log(h)
        $state.loaded();
      }).catch(error => {
        console.log(error)
        $state.error();
      })
    }
  }
}
</script>