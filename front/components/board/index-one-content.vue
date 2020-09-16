<template>
  <section class="content row border-bottom">
    <h4 class="col-12 my-1"><a>{{message.title}}</a></h4>
    <div class="col-12">
      <span class="float-left date small p-1">{{message.created_at}}</span>
      <span class="float-left ml-4 whosent">{{message.writer}}</span>
      <span class="float-right star">
        <img src="/static/img/star_yl.png" width="16" height="16" v-if="message.is_bookmarked">
        <img src="/static/img/star_bk.png" width="16" height="16" v-else>
      </span>
    </div>
    <article class="col-12 my-2">
      {{message.content | trim}}
    </article>
  </section>
</template>

<script>
export default {
  props: {
    message: {type: Object, required: true},
  },
  filters: {
    trim (value) {
      // 「全回メーリス失礼します」の冒頭を削除
      let count = value.indexOf('\n');
      if (count < 0) {
        count = 0;
      }
      return value.slice(count, count+200);
    }
  }
}
</script>

<style scoped>
.content article{
  display: block;
  white-space: nowrap;
  text-overflow: ellipsis;
  overflow: hidden;
}
</style>