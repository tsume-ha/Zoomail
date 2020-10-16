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
    isInitial: true,
  }),
  computed: {
    messages () {
      return this.$store.state.read.messages;
    }
  },
  created () {
    console.log('com _ created')
    console.log('com _ ' + String(this.messages.length))
    if (this.messages.length > 0) {
      return;
    }
    this.$store.dispatch('read/loadMessages').then(() => {
      console.log('com _ created finish')
    })
  },
  methods: {
    async infiniteLoad ($state) {
      console.log('com _ infinite load axios start')
      await this.$store.dispatch('read/loadMessages')
        console.log('com _ vuex.then')
        $state.loaded();

    }
  }
}
</script>