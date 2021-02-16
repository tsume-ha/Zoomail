<template>
  <div>
    <h3>メーリス送信</h3>
    <div id="process-wrapper" class="col-sm-12 col-md-10 col-lg-8 my-5 py-5">
      <h4 v-if="!complete">送信中</h4>
      <h4 v-else>送信完了！</h4>
      <transition mode="out-in">
        <div v-if="progress < 100" key="uploading">
          サーバーにデータを転送中（{{progress}}%）
        </div>
        <div v-else-if="!complete" key="processing">
          サーバーからメーリスを送信中...
        </div>
        <div v-else-if="complete" key="complete">
          メーリスが{{complete_num}}件送信されました
        </div>
      </transition>
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
.v-enter-active, .v-leave-active{
  transition: margin,opacity .3s;
}
.v-enter{
  margin-top: 10px;
  margin-bottom: -10px;
  opacity: 0;
}
.v-enter-to, .v-leave{
  margin-top: 0;
  margin-bottom: 0;
  opacity: 1;
}
.v-leave-to{
  margin-top: -10px;
  margin-bottom: 10px;
  opacity: 0;
}
</style>