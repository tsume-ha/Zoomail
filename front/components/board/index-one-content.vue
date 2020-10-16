<template>
  <section class="content row border-bottom" :id="'message-id-'+String(message.id)">
    <h4 class="col-12 my-1"><router-link :to="link">{{message.id}}</router-link></h4>
    <div class="col-12">
      <span class="float-left date small p-1">{{message.created_at}}</span>
      <span class="float-left ml-4 whosent">{{message.writer}}</span>
      <bookmark-star :id="Number(message.id)" :is_bookmarked="message.is_bookmarked" />
    </div>
    <article class="col-12 my-2">
      {{message.content | trim}}
    </article>
  </section>
</template>

<script>
import bookmarkStar from './bookmark-star.vue'
export default {
  props: {
    message: {type: Object, required: true},
  },
  components: {
    bookmarkStar
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
  },
  computed: {
    link () {
      return './content/' + String(this.message.id) + '/'
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