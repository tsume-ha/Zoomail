<template>
  <div class="attachent-wrapper p-0 my-2"
    @dragenter="dragEnter"
    @dragleave="dragLeave"
    @dragover.prevent
    @drop.prevent="dropFile" 
  >
    <label for="attachment-input" class="my-0" :class="{'attachment-opened':opened}">
      <span v-if="opened">ここに添付するファイルをドロップ</span>
      <span v-else>添付ファイルを選択、もしくはここにドラッグ＆ドロップ</span>
      <input type="file" multiple id="attachment-input" ref="attachments" @change="onFileChange">
    </label>
    <ul class="attachment-list my-0">
      <li v-for="file in files" :key="file.name">
        {{file.name}}
      </li>
    </ul>
    <div v-if="files.length>0">
      {{files.length}}件が選択されています
    </div>
  </div>
</template>

<script>
export default {
  data: () => ({
    opened: false,
    files: [],
  }),
  methods: {
    onFileChange () {
      let files = this.$refs.attachments.files;
      console.log(files)
      this.files = files;
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
      this.files = [...event.dataTransfer.files]
    }
  },
}
</script>

<style scoped>
.attachent-wrapper *{
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
</style>