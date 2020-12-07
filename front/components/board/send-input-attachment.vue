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
      <input type="file" multiple id="attachment-input" ref="attachments" @change="onFileChange">
    </label>
    <div v-if="files.length>0" class="small text-secondary mx-2">
      クリックすると新しいタブでファイルを確認できます
    </div>
    <div class="attachment-preview">
      <div class="attachment-preview-wrapper"
          v-for="file in files"
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
    <div v-if="files.length>0">
      {{files.length}}件が選択されています
    </div>
  </div>
</template>

<script>
import attachmentPreview from "./send-input-attachment-preview";
export default {
  data: () => ({
    opened: false,
    files: [],
  }),
  components: {
    attachmentPreview
  },
  methods: {
    onFileChange () {
      let files = this.$refs.attachments.files;
      console.log(files)
      for (const file of files) {
        this.files.push(file);
      }
    },
    dragEnter (e) {
      console.log('Enter Drop Area');
      this.opened = true;
    },
    dragLeave (e) {
      console.log('leave Drop Area');
      this.opened = false;
    },
    dropFile (e) {
      console.log('Drop File');
      this.opened = false;
      console.log(event.dataTransfer.files)
      // this.files = [...event.dataTransfer.files]
      for (const file of event.dataTransfer.files) {
        this.files.push(file);
      }
    },
    cansel (file) {
      const i = this.files.indexOf(file);
      this.files.splice(i, 1);
    }
  },
}
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
}
.file-cansel:hover{
  background-color: rgb(250, 75, 75);
}

</style>