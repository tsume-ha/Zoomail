<template>
  <div>
    <h3>メーリス送信</h3>
    <div id="process-wrapper" class="col-sm-12 col-md-10 col-lg-8 my-5 py-5">
      <h4 v-if="!complete">送信中</h4>
      <h4 v-else>送信完了！</h4>
      <div v-if="progress < 100">
        サーバーにデータを転送中（{{progress}}%）
      </div>
      <div v-else-if="!complete">
        サーバーからメーリスを送信中...
      </div>
      <div v-else-if="complete">
        メーリスが{{complete_num}}件送信されました
      </div>
    </div>
    <button
      @click="onclick"
      class="btn"
      :class="{'btn-info': complete, 'btn-secondary': !complete}"
      >
      メーリス一覧に戻る
    </button>
  </div>
</template>

<script>
export default {
  computed: {
    progress () {
      return this.$store.state.send.progress;
    },
    complete () {
      return this.$store.state.send.complete;
    },
    complete_num () {
      return this.$store.state.send.complete_num;
    },
  },
  methods: {
    onclick () {
      if (!this.complete) {
        return false
      }
      window.location.href='/read/';
    }
  }
}
</script>

<style scoped>
#process-wrapper{
  border: 1px #eeeeee dotted;
  text-align: center;
}
</style>