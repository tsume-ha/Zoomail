<template>
  <section>
    <h3>メーリス送信確認</h3>

    <div class="col-sm-12 col-md-10 col-lg-8 py-1 px-0 my-2 mx-0 display-wraper">
      <div class="p-1 label">件名：</div>
      <div class="p-1 border rounded display">{{title}}</div>
    </div>

    <div class="col-sm-12 col-md-10 col-lg-8 py-1 px-0 my-2 mx-0 display-wraper">
      <div class="p-1 label">送信先：</div>
      <div class="p-1 border rounded display">
        <span v-for="obj in tos" :key="obj.label" class="badge badge-pill badge-light mx-2 border rounded">{{obj.label}}</span>
      </div>
    </div>

    <div class="col-sm-12 col-md-10 col-lg-8 py-1 px-0 my-2 mx-0 display-wraper">
      <div class="p-1 label">本文：</div>
      <div class="p-1 border rounded display" style="white-space: pre-wrap;" v-text="content">
      </div>
    </div>

    <div v-if="attachments.length" class="col-sm-12 col-md-10 col-lg-8 py-1 px-0 my-2 mx-0 display-wraper">
      <div class="p-1 label">添付ファイル：</div>
      <div class="p-1 border rounded display attachment-wraper">
        <attachment-preview
          v-for="file in attachments"
          :key="file.name+file.size"
          :file="file"
        />
        <div class="mx-2">{{attachments.length}}件添付</div>
      </div>
    </div>

    <div class="col-sm-12 col-md-10 col-lg-8 py-1 px-0 my-4 mx-0" id="send-button-wraper">
      <button @click="backToInput" class="btn btn-secondary">戻る</button>
      <button @click="send" class="btn btn-info">送信する</button>
    </div>
  </section>
</template>

<script>
import { computed } from 'vue'
import { useStore } from "vuex"
import { useRouter } from 'vue-router'
import attachmentPreview from "./components/send-input-attachment-preview";
export default {
  components: {
    attachmentPreview
  },
  setup() {
    const store = useStore();
    const router = useRouter();
    if (!store.getters['send/isValidAndDirty']) {
      store.commit('message/addMessage', {
        level: "warning",
        message: "フォームに正しく入力してください。",
        appname: "mail/send"
      });
      router.push('/mail/send');
    }
    const title = computed(() => store.state.send.title.value)
    const content = computed(() => store.state.send.content.value)
    const writer = computed(() => store.state.send.writer.value)
    const attachments = computed(() => store.state.send.attachments.value)
    const tos = computed(() => [{ year: 0, label: "全回メーリス" }])

    const backToInput = e => {
      e.preventDefault();
      router.push('/mail/send');
    }
    const send = e => {
      e.preventDefault();
      // send to server.
      console.log('send')
    }
    return{
      title, content, writer, attachments, tos,
      backToInput, send
    }
  }
  // components: {
  //   attachmentPreview
  // },
  // methods: {
  //   backToInput () {
  //     this.$emit('backToInput');
  //   },
  //   send () {
  //     this.$emit('send');
  //   }
  // },
  // computed: {
  //   title () {
  //     return this.$store.state.send.title;
  //   },
  //   content () {
  //     return this.$store.state.send.content;
  //   },
  //   to () {
  //     return this.$store.state.send.to;
  //   },
  //   to_groups () {
  //     return this.$store.state.send.to_groups;
  //   },
  //   to_selected () {
  //     return this.to_groups.filter(obj => this.to.includes(obj.year));
  //   },
  //   attachments () {
  //     return this.$store.state.send.attachments;
  //   },
  // }
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

.attachment-wraper{
  display: flex;
  flex-wrap: wrap;
  align-items: baseline;
}
</style>