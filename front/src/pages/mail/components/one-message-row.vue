<template>
  <section class="content row border-bottom" :id="'message-id-'+String(message.id)">
    <h4 class="col-12 my-1"><router-link :to="link">{{String(message.id)}} - {{message.title}}</router-link></h4>
    <div class="col-12">
      <span class="float-left date small p-1">{{message.created_at}}</span>
      <span class="float-left ml-4 whosent">{{message.writer}}</span>
      <span class="float-right" @click="bookmark">
        <img src="/static/img/star_yl.png" width="16" height="16" v-if="message.is_bookmarked">
        <img src="/static/img/star_bk.png" width="16" height="16" v-else>
      </span>
    </div>
    <article class="col-12 my-2">
      {{trimed}}
    </article>
  </section>
</template>

<script>
import { computed } from 'vue';
import { useStore } from "vuex";
export default {
  props: {
    message: {required: true, type: Object}
  },
  setup(props) {
    const store = useStore();

    const message = computed(() => props.message);
    const trimed = computed(() => {
      const text = message.value.content;
      let count = text.indexOf('\n');
      if (count < 0) {
        count = 0;
      }
      return text.slice(count, count+200);
    });
    const link = computed(() => '/mail/' + String(message.value.id));

    const bookmark = () => {
      store.dispatch('read/toggleBookmark', message.value.id);
    };
    return {
      bookmark,
      trimed, link
    };
  }
};
</script>

<style scoped>
.content article{
  display: block;
  white-space: nowrap;
  text-overflow: ellipsis;
  overflow: hidden;
}
section h4 a{
	color: #0058B3;
}
section:hover h4 a{
	color: #0058B3;
}
</style>