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
  created () {
    // 発火するのは次の2パターン
    // - /read/にアクセスしてきたとき
    //   -> Vuexは初期状態で、`this.messages.length === 0`
    // - /read/content/(number)から戻ってきたとき
    //   -> Vuexにmessagesが残ってる。APIを叩かない。
    if (this.messages.length > 0) {
      return;
    }
    this.$store.dispatch('read/loadMessages');
    // この書き方だとVuexが初期状態のときに
    // 下のmethods.infiniteLoadも発火するので
    // APIは2回叩かれますが、これは仕様です。
  },
  methods: {
    infiniteLoad ($state) {
      this.$store.dispatch('read/loadMessages').then(() => {
        $state.loaded();
      });
    }
  }
}
</script>