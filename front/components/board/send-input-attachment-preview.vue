<template>
  <div class="preview-content-wrapper">
    <img v-if="isImage" src="/static/img/board/file-icon.png" alt="iamge-preview">
    <img v-else-if="file.type=='application/pdf'" src="/static/img/board/pdf-icon.png" alt="pdf-icon">
    <img v-else src="/static/img/board/file-icon.png" alt="file-icon">
    <div class="preview-file-name">{{file.name}}</div>
  </div>
</template>

<script>
export default {
  data: () => ({
  }),
  props: {
    file: {required: true, type: File}
  },
  computed: {
    isImage () {
      return this.file.type.indexOf('image') > -1;
    }
  }
}
</script>

<style scoped>
.preview-content-wrapper{
  border: 1px solid #aaa;
  border-radius: 4px;
  width: 140px;
  max-height: 180px;
  margin: 0.5rem;
  padding: 0.5rem;
  overflow: hidden;
}
img{
  width: auto;
  margin: 0 auto;
  height: 100px;
  display: block;
}
.preview-file-name{
  font-size: 10px;
}
</style>