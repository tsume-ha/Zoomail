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
      spinner="circles"
      :identifier="searchData"
      @infinite="infiniteLoad"
    >
      <div
        slot="no-more"
        class="text-center alert alert-secondary my-2 p-2">
        メーリスは以上です
      </div>
      <div
        slot="no-results"
         class="text-center alert alert-secondary my-2 p-2">
         表示できるメーリスはありませんでした
      </div>
    </infinite-loading>
    <div id="sendlink">
      <a href="/send/">
        <span>メーリスを送信する</span>
        <img src="/static/img/send.svg" height="50" width="50">
      </a>
    </div>
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
    },
    search (data) {
      this.$store.commit('read/clearMessages')
      this.searchData = data;
      // identiferが変更され、自動でinfiniteLoadが発火する
    }
  }
}
</script>

<style scoped>
div#sendlink{
  position: fixed;
  bottom: 3rem;
  right: 8vw;
  z-index: 10;
}

div#sendlink a{
  display: block;
  position: relative;
  height: 62px;
  padding: 5px 16px;
  border: 1px solid #3bc665;
  border-radius: 33px;
  text-decoration: none;
  background-color: rgba(255,255,255,0.5);
  transition: 0.4s;
  overflow: hidden;
}


div#sendlink a span{
  display: none;
  text-decoration: none;
  color: #212529;
}

div#sendlink a.hover{
  border: 1px double #3bc665;
  background-color: #ccf0d7;
}

div#sendlink a.hover span{
  display: inline;
}

div#sendlink a img{
  transform: scale(-1, 1);
  margin: 0 -4px 0 0;
  padding: 0 -3px;
}
</style>