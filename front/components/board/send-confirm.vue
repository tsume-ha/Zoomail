<template>
  <section>
    <h3>メーリス送信確認</h3>

    <div class="col-sm-12 col-md-10 col-lg-8 py-1 px-0 my-2 mx-0 display-wraper">
      <div class="p-1 label">件名：</div>
      <div class="p-1 border rounded display">タイトル</div>
    </div>

    <div class="col-sm-12 col-md-10 col-lg-8 py-1 px-0 my-2 mx-0 display-wraper">
      <div class="p-1 label">送信先：</div>
      <div class="p-1 border rounded display">24期（会長：だれだれ）, 25期（会長：だれだれ）</div>
    </div>

    <div class="col-sm-12 col-md-10 col-lg-8 py-1 px-0 my-2 mx-0 display-wraper">
      <div class="p-1 label">本文：</div>
      <div class="p-1 border rounded display" style="white-space: pre-wrap;" v-text="content">
      </div>
    </div>

    <div class="col-sm-12 col-md-10 col-lg-8 py-1 px-0 my-2 mx-0 display-wraper">
      <div class="p-1 label">添付ファイル：</div>
      <div class="p-1 border rounded display">2件添付</div>
    </div>

    <div class="col-sm-12 col-md-10 col-lg-8 py-1 px-0 my-4 mx-0" id="send-button-wraper">
      <button @click="backToInput" class="btn btn-secondary">戻る</button>
      <button @click="send" class="btn btn-info">送信する</button>
    </div>
  </section>
</template>

<script>
export default {
  methods: {
    backToInput () {
      this.$emit('backToInput');
    },
    send () {
      return false;
    }
  },
  data: () => ({
    content: `本文本文本文本文本文本文本文本文本文
本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文

本文本文  本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本
文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文本文`
  })
}
</script>

<style scoped>
.display-wraper{
  display: flex;
}
.display-wraper .label{
  flex-grow: 0;
  flex-shrink: 0;
  flex-basis: auto;
}
.display-wraper .display{
  flex-grow: 2;
  flex-shrink: 2;
  flex-basis: auto;
}
#send-button-wraper{
  display: flex;
  justify-content: space-between;
}
</style>