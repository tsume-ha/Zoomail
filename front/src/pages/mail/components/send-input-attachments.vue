<template>
  <div class="attachent-wrapper p-0 my-2">
    <label
      for="attachment-input"
      class="my-0"
      :class="{'attachment-opened':opened}"
      @dragenter="dragEnter"
      @dragleave="dragLeave"
      @dragover.prevent
      @drop.prevent="dropFile"
    >
      <span v-if="opened">ここに添付するファイルをドロップ</span>
      <span v-else>添付ファイルを選択、もしくはここにドラッグ＆ドロップ</span>
      <input type="file" multiple id="attachment-input" @change="onFileChange">
    </label>
    <div v-if="attachments.length>0" class="small text-secondary mx-2">
      クリックすると新しいタブでファイルを確認できます
    </div>
    <div class="attachment-preview">
      <div class="attachment-preview-wrapper"
          v-for="file in attachments"
          :key="file.name+file.size"
        >
        <attachment-preview
        :file="file"
        />
        <div
          class="file-cansel"
          @click="cansel(file)"
        >×</div>
      </div>
    </div>
    <div v-if="attachments.length>0" class="mx-2">
      {{attachments.length}}件が選択されています
    </div>
    <validation-error-messages
      v-if="error_messages.length > 0 && is_dirty"
      :messages="error_messages" />
  </div>
</template>

<script>
import validationErrorMessages from '../../../components/validation-error-messages.vue';
import attachmentPreview from './send-input-attachment-preview.vue';
import { computed, onBeforeMount, ref } from 'vue';
import { useStore } from "vuex";
export default {
  components: {
    validationErrorMessages,
    attachmentPreview
  },
  setup() {
    // Vuex
    const store = useStore();
    const attachments = computed({
      get: () => store.state.send.attachments["value"],
      set: value => store.commit('send/setAttachments', value)
    });
    const is_dirty = computed(() => store.state.send.attachments["is_dirty"]);
    const error_messages = computed(() => store.state.send.attachments["error_messages"]);

    // display variable
    const opened = ref(false);

    // methods
    const internalAttachments = ref([]);
    const onFileChange = inputFile => {
      const files = inputFile.target.files;
      for (let i = 0; i < files.length; i++) {
        internalAttachments.value.push(files[i]);
      }
      commit();
    };
    const dragEnter = () => { opened.value = true; };
    const dragLeave = () => { opened.value = false; };
    const dropFile = e => {
      opened.value = false;
      const files = e.dataTransfer.files;
      for (let i = 0; i < files.length; i++) {
        internalAttachments.value.push(files[i]);
      }
      commit();
    };
    const cansel = file => {
      internalAttachments.value = internalAttachments.value.filter(f => {
        return !(f.size === file.size && f.name === file.name);
      });
      commit();
    };

    const commit = () => {
      // 重複してるファイルを取り除いて、Vuexに投げる
      const uniques = internalAttachments.value.reduce((prev, current) => {
        if (!prev.some(f => (f.size === current.size && f.name === current.name))) {
          return [...prev, current];
        } else {
          // 重複あり
          store.commit('message/addMessage', {
            level: "warning",
            message: "重複したファイルが検出されました。" + current.name + "は追加されていません。",
            appname: "mail/send"
          });
          return [...prev];
        }
      }, []);
      internalAttachments.value.length = 0;
      // internalAttachmentsの上書き
      uniques.forEach(f => { internalAttachments.value.push(f); });
      store.commit('send/setAttachments', uniques);
    };

    onBeforeMount(() => {
      // confirmから戻ってきたときにVuexから取得する
      attachments.value.forEach(a => {
        internalAttachments.value.push(a);
      });
    });

    return {
      attachments, is_dirty, error_messages,
      opened, internalAttachments,
      onFileChange, dragEnter, dragLeave, dropFile, cansel
    };
  }
};
</script>

<style scoped>
.attachent-wrapper label *{
  pointer-events: none;
}

.attachent-wrapper > label{
  display: inline-block;
  border: 1px dotted #d6eef5;
  border-radius: 4px;
  background-color: #f1f9fc;
  padding: 0.5rem 1rem;
  transition: .5s;
}
.attachent-wrapper > label.attachment-opened{
  display: block;
  width: 100%;
  text-align: center;
  padding: 4rem;
}

#attachment-input{
  display: none;
}

.attachment-preview{
  display: flex;
  flex-wrap: wrap;
  align-items: baseline;
}
.attachment-preview-wrapper{
  position: relative;
}

.file-cansel{
  position: absolute;
  text-align: center;
  top: 0;
  right: 0;
  border: 1px solid #aaa;
  border-radius: 4px;
  margin: 0.5rem;
  width: 32px;
  height: 32px;
  line-height: 30px;
  font-size: 20px;
  background-color: rgba(255, 255, 255, 0.4);
  transition: .2s;
  z-index: 2;
  cursor: pointer;
}
.file-cansel:hover{
  background-color: rgba(255, 255, 255, 0.95);
}

</style>