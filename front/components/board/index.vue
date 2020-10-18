<template>
  <div>
    <h3>メーリス一覧</h3>
    <one-content
      v-for="message in messages"
      :key="message.id"
      :message="message" />
    <infinite-loading
      @infinite="infiniteLoad"
    >
      <div slot="no-more">メーリスは以上です</div>
      <div slot="no-results">表示できるメーリスはありませんでした</div>
    </infinite-loading>
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
      this.$store.dispatch('read/loadMessages').then(response => {
        console.log(response)
        if (this.messages.length > 0) {
          $state.loaded();          
        }
        if (response.has_next === false) {
          $state.complete();
        }
      }).catch(error => {
        console.log(error)
        $state.error();
      })
    }
  }
}
</script>