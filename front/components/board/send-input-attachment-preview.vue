<template>
  <div class="preview-content-wrapper" @click="openFile">
    <img v-if="isImage" :src="imageURL" alt="iamge-preview">
    <img v-else-if="file.type=='application/pdf'" src="/static/img/board/pdf-icon.png" alt="pdf-icon">
    <img v-else src="/static/img/board/file-icon.png" alt="file-icon">
    <div class="preview-file-name">{{file.name}}</div>
  </div>
</template>

<script>
export default {
  data: () => ({
    imageURL: "",
    objectURL: "",
  }),
  props: {
    file: {required: true, type: File}
  },
  computed: {
    isImage () {
      return this.file.type.startsWith('image/');
    }
  },
  methods: {
    readImage () {
      let reader = new FileReader();
      reader.onload = this.loadImage;
      reader.readAsDataURL(this.file)
      this.objectURL = URL.createObjectURL(this.file);
    },
    loadImage (e) {
      let image = new Image();
      this.imageURL = e.target.result;
    },
    openFile () {
      if (this.objectURL) {
        window.open(this.objectURL, "filePreview")
      }
    }
  },
  mounted () {
    this.readImage();
  },
  beforeDestroy () {
    URL.revokeObjectURL(this.file);
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
  margin: 0 auto;
  height: 100px;
  display: block;
}
.preview-file-name{
  font-size: 10px;
}
</style>