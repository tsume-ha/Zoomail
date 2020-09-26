<template>
  <div v-if="!messageExists">
    <!-- message does not exist -->
    message does not exist
  </div>
  <div v-else>
    <!-- message exists -->
    <div class="message-title mb-2">
      <router-back-arrow :href="'../../'" />
      <h4 class="d-inline-block m-0">{{message.title}}</h4>
    </div>
    <div class="col-sm-12 col-md-8 mt-1 pl-0">
      <span class="date d-inline-block">{{message.created_at}}</span>
      <span class="ml-4 whosent">{{message.writer}}</span>
      <bookmark-star :id="Number(message.id)" :is_bookmarked="message.is_bookmarked" />
    </div>
    <hr>
    <p class="content" v-text="message.content"></p>

    <template v-if="message.writer!=message.sender">
    <hr>
    <p class="small">このメーリスは {{message.sender}} によって代理送信されました。</p>
    </template>

    <hr>

  </div>
</template>

<script>
import bookmarkStar from './bookmark-star.vue'
import routerBackArrow from './router-back-arrow.vue'
export default {
  props: {
    id: {type: Number, required: true}
  },
  components: {
    bookmarkStar,
    routerBackArrow
  },
  data: () => ({
    messageExists: false,
    message: {},
  }),
  created () {
    let message = this.$store.state.read.messages.find(obj => obj.id == this.id);
    if (message) {
      this.messageExists = true;
      this.message = message;
    }
    // 直接アクセスして来た場合
    console.log('直接アクセス')
    this.axios.get('/read/api/content/' + String(this.id) + '/')
      .then(res => {
        console.log(res);
        this.messageExists = true;
        this.message = res.data.message_list[0];
      })
      .catch(error => {
        console.log(error)
      })
    this.$store.dispatch('read/loadMessages');
  },


}
</script>

<style scoped>
.message-title > *{
  vertical-align: bottom;
}
p.content{
  white-space: pre-line;
}
</style>