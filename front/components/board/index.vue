<template>
  <div>
    <h3>メーリス一覧</h3>
    <searchform
      @search="search"
     />
    <one-content
      v-for="message in messages"
      :key="message.id"
      :message="message" />
    <infinite-loading
      :identifier="searchData"
      @infinite="infiniteLoad"
    >
      <div slot="no-more" class="text-center alert alert-secondary my-2 p-2">メーリスは以上です</div>
      <div slot="no-results">表示できるメーリスはありませんでした</div>
    </infinite-loading>
  </div>
</template>

<script>
import oneContent from './index-one-content.vue';
import searchform from './index-searchform.vue';
export default {
  name: 'index',
  components: {
    oneContent,
    searchform
  },
  data: () => ({
    searchData: {}
  }),
  computed: {
    messages () {
      return this.$store.state.read.messages;
    }
  },
  methods: {
    infiniteLoad ($state) {
      console.log($state)
      this.$store.dispatch('read/loadMessages', this.searchData).then(response => {
        // console.log(response)
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
    },
    search (data) {
      this.$store.commit('read/clearMessages')
      this.searchData = data;
      // identiferが変更され、自動でinfiniteLoadが発火する
    }
  }
}
</script>