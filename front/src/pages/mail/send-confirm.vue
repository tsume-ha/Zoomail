<template>
  <article>
    <h3>メーリス送信確認</h3>

    <section class="card">
      <div class="pure-g">
        <div class="pure-u-1 pure-u-sm-1-5 pure-u-md-5-24">件名</div>
        <div class="pure-u-1 pure-u-sm-4-5 pure-u-md-19-24">{{ title }}</div>
      </div>

      <div class="pure-g">
        <div class="pure-u-1 pure-u-sm-1-5 pure-u-md-5-24">From</div>
        <div class="pure-u-1 pure-u-sm-4-5 pure-u-md-19-24">
          {{ writer.name }} ({{ writer.year }})
        </div>
      </div>

      <div class="pure-g">
        <div class="pure-u-1 pure-u-sm-1-5 pure-u-md-5-24">To</div>
        <div class="pure-u-1 pure-u-sm-4-5 pure-u-md-19-24">
          <span v-for="obj in tos" :key="obj.label" class="to-address">{{
            obj.label
          }}</span>
        </div>
      </div>

      <div class="pure-g">
        <div class="pure-u-1 pure-u-sm-1-5 pure-u-md-5-24">本文</div>
        <div class="pure-u-1 pure-u-sm-4-5 pure-u-md-19-24 message-content">
          {{ content }}
        </div>
      </div>

      <div class="pure-g">
        <div class="pure-u-1 pure-u-sm-1-5 pure-u-md-5-24">添付ファイル</div>
        <div class="pure-u-1 pure-u-sm-4-5 pure-u-md-19-24">
          <div v-if="attachments.length" class="attachment-wraper">
            <AttachmentPreview
              v-for="file in attachments"
              :key="file.name + file.size"
              :file="file"
            />
            <div>{{ attachments.length }}件添付</div>
          </div>
          <div v-else>添付ファイルはありません</div>
        </div>
      </div>
    </section>
    <div class="custom-two-buttons-wrapper">
      <router-link :to="{ name: 'mail:send' }" class="pure-button return">
        戻る
      </router-link>
      <router-link
        :to="{ name: 'mail:send-finish' }"
        class="pure-button button-primary"
      >
        送信する
      </router-link>
    </div>
  </article>
</template>

<script>
import { computed } from "vue";
import { useStore } from "vuex";
import { useRouter } from "vue-router";
import AttachmentPreview from "./components/send-input-attachment-preview";
export default {
  components: {
    AttachmentPreview,
  },
  setup() {
    const store = useStore();
    const router = useRouter();
    if (!store.getters["send/isValidAndDirty"]) {
      store.commit("message/addMessage", {
        level: "warning",
        message: "フォームに正しく入力してください。",
        appname: "mail/send",
      });
      router.push("/mail/send");
    }
    const title = computed(() => store.state.send.title.value);
    const tos = computed(() => store.state.send.tos.value);
    const content = computed(() => store.state.send.content.value);
    const writer = computed(() => store.state.send.writer.value);
    const attachments = computed(() => store.state.send.attachments.value);

    const backToInput = (e) => {
      e.preventDefault();
      router.push("/mail/send");
    };
    const send = (e) => {
      e.preventDefault();
    };
    return {
      title,
      content,
      writer,
      attachments,
      tos,
      backToInput,
      send,
    };
  },
};
</script>

<style lang="scss" scoped>
section.card {
  padding: 1rem;

  > div {
    margin: 0 0 1rem;
    > div {
      margin: 0 0 0.5rem;
    }
  }

  span.to-address {
    display: inline-block;
    background-color: $bg-light-lighten3;
    border-radius: 0.5rem;
    padding: 0.25rem;
    margin: 0 0.25rem 0.25rem 0;
    line-height: 1.5;
  }
  div.message-content {
    white-space: pre-wrap;
    line-height: 1.5;
    word-break: break-all;
  }

  div.attachment-wraper {
    display: flex;
    flex-wrap: wrap;
    align-items: flex-end;
  }
}
</style>