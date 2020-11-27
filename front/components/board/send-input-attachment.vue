<template>
  <div class="attachent-wrapper col-sm-12 col-md-10 col-lg-8 p-0 my-2">
    <label for="attachment-input" class="my-0 px-3 py-2">
      <span v-if="opened">ここにファイルをドロップ</span>
      <span v-else>添付ファイルを選択</span>
      <input type="file" multiple id="attachment-input" ref="attachments" @change="onFileChange">
    </label>
    <ul class="attachment-list my-0">
      <li v-for="file in files" :key="file.name">
        {{file.name}}
      </li>
    </ul>
    <div v-if="files.length>0">
      以上{{files.length}}件が選択されています
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
    }
  }
}
</script>

<style scoped>
.attachent-wrapper > label{
  display: inline-block;
  border: 1px dotted #d6eef5;
  border-radius: 4px;
  background-color: #f1f9fc;

}
#attachment-input{
  display: none;
}
</style>