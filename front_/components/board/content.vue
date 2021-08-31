<template>
  <div v-if="status.messageLoaded && status.canRead">
    <!-- message exists -->
    <div class="message-title mb-2">
      <router-back-arrow :href="'../../'" />
      <h4 class="d-inline-block m-0">{{message.title}}</h4>
    </div>
    <div class="col-sm-12 col-md-8 my-1 pl-0">
      <span class="date d-inline-block">{{message.created_at}}</span>
      <span class="ml-4 whosent">{{message.writer}}</span>
      <bookmark-star :id="Number(message.id)" :is_bookmarked="message.is_bookmarked" />
    </div>
    <hr>
    <div
      class="col-sm-12 col-md-8 content p-0"
      v-html="message.html"
      ></div>
    <template v-if="attachments.length>0">
    <hr>
    <div class="col-sm-12 col-md-8 my-1 pl-0">
      <h6>添付ファイル</h6>
      <template v-for="file in attachments">
        <img v-if="file.is_image" :src="file.path" style="width: 100%;max-width: 560px;" :key="file.pk" />
        <a v-else :href="'/api/board/download/' + id + '/' +file.pk+'/'" :key="file.pk">
          {{file.filename}}
        </a>
      </template>
    </div>
    </template>
    <template v-if="message.writer!=message.sender">
    <hr>
    <p class="small">このメーリスは {{message.sender}} によって代理送信されました。</p>
    </template>

    <hr>

  </div>

  <div v-else-if="!status.messageLoaded">
    <!-- ローディング中 -->
    Now loading...
  </div>
  <div v-else-if="!status.canRead">
    <!-- message does not exist -->
    You can not read this message or message does not exist.
  </div>
  <div v-else>
    some error occured
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
  metaInfo() {
    const message = this.message;
    return {
      title: message.title
    }
  },
  data: () => ({
    status: {
      messageLoaded: false,
      canRead: false,
    },
    message: {},
    attachments: [],
  }),
  created () {
    // attachmentsなどのデータ
    this.axios.get('/api/board/contentothers/' + String(this.id) + '/')
      .then(res => {
        console.log(res)
        this.attachments = res.data.attachments;
      })
      .catch(error => {
        console.log(error)
      })

    // messageデータ
    let message = this.$store.state.read.messages.find(obj => obj.id == this.id);
    if (message) {
      this.$set(this.status, 'messageLoaded', true);
      this.$set(this.status, 'canRead', true);
      this.message = message;
      return;
    }
    // 直接アクセスして来た場合
    console.log('直接アクセス')
    this.axios.get('/api/board/content/' + String(this.id) + '/')
      .then(res => {
        this.message = res.data.message;
        this.$set(this.status, 'messageLoaded', true);
        this.$set(this.status, 'canRead', true);
      })
      .catch(error => {
        console.log(error)
        this.$set(this.status, 'messageLoaded', true);
        this.$set(this.status, 'canRead', false);
      })
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